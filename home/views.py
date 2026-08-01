import json
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone


def _letter_grade(pct):
    """Rough percentage -> letter mapping, used only where the real
    Course model doesn't already expose a computed letter grade.
    Swap this out if SmartStudy uses a different scale."""
    if pct is None:
        return None
    if pct >= 93: return "A"
    if pct >= 90: return "A-"
    if pct >= 87: return "B+"
    if pct >= 83: return "B"
    if pct >= 80: return "B-"
    if pct >= 77: return "C+"
    if pct >= 70: return "C"
    if pct >= 60: return "D"
    return "F"


def home(request):
    if request.user.is_authenticated:
        return redirect("home:dashboard")
    return render(request, "home/index.html")


@login_required
def dashboard(request):
    """
    Landing page shown right after login/register. Surfaces the Stats +
    Analytics block from UniTracker, Stats + Course Grades from SmartStudy,
    Calendar feed + skill-gap teaser from CampusPulse, and Stats + Recent
    Running History from CampusCribs.

    Budget is reused directly from BudgetDashboardView, so those numbers
    are exact. UniTracker / SmartStudy / CampusPulse are best-guess against
    field names visible in their templates — wrapped in try/except so a
    mismatch just hides that section instead of erroring. Send over the
    real models.py/views.py for those three and I'll make it exact.
    """
    context = {}

    # ---------- UniTracker: Stats + Analytics ----------
    try:
        from universities.models import University
        apps_qs = University.objects.filter(user=request.user)

        uni_reach = apps_qs.filter(tier__iexact="REACH").count()
        uni_match = apps_qs.filter(tier__iexact="MATCH").count()
        uni_safety = apps_qs.filter(tier__iexact="SAFETY").count()

        context["uni_total"] = apps_qs.count()
        context["uni_reach"] = uni_reach
        context["uni_match"] = uni_match
        context["uni_safety"] = uni_safety
        context["uni_submitted"] = apps_qs.filter(status__iexact="SUBMITTED").count()
        context["uni_accepted"] = apps_qs.filter(status__iexact="ACCEPTED").count()
        context["uni_interview"] = apps_qs.filter(status__iexact="INTERVIEW").count()
        context["uni_due_soon"] = apps_qs.filter(
            deadline__isnull=False,
            deadline__gte=timezone.now().date(),
            deadline__lte=timezone.now().date() + timedelta(days=30),
        ).count()

        timeline = list(apps_qs.exclude(deadline__isnull=True).order_by("deadline")[:8])
        today = timezone.now().date()
        labels, days = [], []
        for u in timeline:
            labels.append(u.name)
            try:
                days.append((u.deadline - today).days)
            except Exception:
                days.append(0)

        context["uni_timeline_labels"] = json.dumps(labels)
        context["uni_timeline_days"] = json.dumps(days)
        context["uni_status_counts"] = json.dumps([uni_reach, uni_match, uni_safety])
        context["uni_next"] = timeline[0] if timeline else None
    except Exception:
        pass

    # ---------- SmartStudy: Stats + Course Grades ----------
    try:
        from smart_study.models import Course, Assignment, PomodoroSession
        courses = Course.objects.filter(user=request.user)

        context["study_total_courses"] = courses.count()
        context["study_total_assignments"] = Assignment.objects.filter(course__user=request.user).count()
        context["study_pomodoro_count"] = PomodoroSession.objects.filter(
            user=request.user, completed=True
        ).count()

        rows, grades = [], []
        for c in courses:
            grade = getattr(c, "current_grade", None)
            if grade is not None:
                grades.append(grade)
            rows.append({
                "name": c.name,
                "color": getattr(c, "color", "#7F77DD"),
                "grade": grade,
                "letter": _letter_grade(grade),
                "pk": c.pk,
            })
        context["study_course_rows"] = rows[:5]
        avg = round(sum(grades) / len(grades), 1) if grades else None
        context["study_avg_grade"] = avg
        context["study_avg_letter"] = _letter_grade(avg) if avg is not None else "—"
    except Exception:
        pass

    # ---------- CampusPulse: Calendar feed + skill-gap ----------
    try:
        from extracurricular.models import ClubMembership, VolunteerLog, ImpactEntry
        memberships = ClubMembership.objects.filter(user=request.user)
        context["pulse_total_clubs"] = memberships.count()
        context["pulse_volunteer_hours"] = (
            VolunteerLog.objects.filter(user=request.user).aggregate(total=Sum("hours"))["total"] or 0
        )
        context["pulse_total_impacts"] = ImpactEntry.objects.filter(user=request.user).count()
        leadership_count = memberships.filter(role__iexact="LEADER").count()
        context["pulse_leadership_count"] = leadership_count
        context["pulse_member_count"] = memberships.count() - leadership_count
    except Exception:
        pass

    # path_analysis and the leadership recommendation text are computed by
    # CampusPulse's own view (a skill-matching algorithm I don't have direct
    # access to). Trying to reuse it directly here — if the real module/
    # function name differs from this guess, this block just no-ops and the
    # card falls back to its "No path analysis logged yet." empty state
    # rather than showing fabricated numbers.
    try:
        from extracurricular.views import campuspulse as _campuspulse_view
        import inspect
        # If campuspulse() is a plain function-based view, its context isn't
        # normally recoverable from the HttpResponse it returns. This only
        # works if it's refactored to expose a `_get_context` alongside it
        # (matching the BudgetDashboardView pattern) — adjust as needed.
        if hasattr(_campuspulse_view, "_get_context"):
            pulse_ctx = _campuspulse_view._get_context(request)
            context["path_analysis"] = pulse_ctx.get("path_analysis")
            context["pulse_leadership_feedback"] = pulse_ctx.get("leadership_feedback")
    except Exception:
        pass

    try:
        # Guessed field name — adjust to wherever the real ical feed token lives.
        token = request.user.profile.ical_feed_token
        context["pulse_feed_url"] = (
            f"{request.scheme}://{request.get_host()}"
            f"{reverse('extracurricular:ical_feed', args=[token])}"
        )
    except Exception:
        pass

    # ---------- CampusCribs: Stats + Recent Running History (real) ----------
    try:
        from budget.views import BudgetDashboardView
        budget_ctx = BudgetDashboardView()._get_context(request)
        context["budget_balance"] = budget_ctx["current_balance"]
        context["budget_runway_days"] = budget_ctx["runway_days"]
        context["budget_days_remaining"] = budget_ctx["days_remaining"]
        context["budget_noodle_alert"] = budget_ctx["noodle_alert"]
        context["budget_entries"] = list(budget_ctx["entries"])[:5]
    except Exception:
        pass

    try:
        from housing.models import Property
        properties = Property.objects.filter(user=request.user)
        context["housing_total"] = properties.count()
        context["housing_signed"] = properties.filter(status="SIGNED").count()
    except Exception:
        pass

    try:
        household = request.user.households.first()
        if household:
            context["household_name"] = household.name
            context["household_member_count"] = household.members.count()
    except Exception:
        pass

    return render(request, "home/dashboard.html", context)


def about(request):
    return render(request, "home/about.html")


def features(request):
    return render(request, "home/features.html")


def help_page(request):
    return render(request, "home/help.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not email or not message:
            messages.error(request, "Please fill in every field before sending.")
            return render(request, "home/contact.html")

        send_mail(
            subject=f"NEXA contact form — {name}",
            message=f"From: {name} <{email}>\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )

        messages.success(request, "Thanks — your message has been sent. We'll get back to you soon.")
        return redirect("contact")

    return render(request, "home/contact.html")