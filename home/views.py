from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.utils import timezone


def home(request):
    if request.user.is_authenticated:
        return redirect("home:dashboard")
    return render(request, "home/index.html")


@login_required
def dashboard(request):
    """
    Landing page shown right after login/register.
    Pulls a handful of headline numbers from each app so the user sees
    something useful at a glance instead of a blank welcome screen.

    Every block below is wrapped in try/except because this view lives
    outside those apps — if a model/field name here doesn't match your
    actual app, that one card just renders without numbers instead of
    crashing the whole dashboard.
    """
    context = {}

    # ---------- UniTracker ----------
    try:
        from universities.models import University
        apps_qs = University.objects.filter(user=request.user)
        context["uni_total"] = apps_qs.count()
        context["uni_submitted"] = apps_qs.filter(status__iexact="SUBMITTED").count()
        context["uni_accepted"] = apps_qs.filter(status__iexact="ACCEPTED").count()
        context["uni_next"] = (
            apps_qs.exclude(deadline__isnull=True)
            .filter(deadline__gte=timezone.now())
            .order_by("deadline")
            .first()
        )
    except Exception:
        pass

    # ---------- SmartStudy ----------
    try:
        from smart_study.models import Course, Assignment, PomodoroSession
        courses = Course.objects.filter(user=request.user)
        context["study_total_courses"] = courses.count()
        context["study_pomodoro_count"] = PomodoroSession.objects.filter(
            user=request.user, completed=True
        ).count()
        context["study_next_assignment"] = (
            Assignment.objects.filter(
                course__user=request.user, due_date__gte=timezone.now()
            )
            .order_by("due_date")
            .first()
        )
        grades = [c.current_grade for c in courses if getattr(c, "current_grade", None)]
        context["study_avg_grade"] = round(sum(grades) / len(grades), 1) if grades else None
    except Exception:
        pass

    # ---------- CampusPulse ----------
    try:
        from extracurricular.models import ClubMembership, VolunteerLog, ImpactEntry
        context["pulse_total_clubs"] = ClubMembership.objects.filter(user=request.user).count()
        context["pulse_volunteer_hours"] = (
            VolunteerLog.objects.filter(user=request.user).aggregate(total=Sum("hours"))["total"] or 0
        )
        context["pulse_total_impacts"] = ImpactEntry.objects.filter(user=request.user).count()
    except Exception:
        pass

    # ---------- CampusCribs ----------
    try:
        from budget.models import Transaction
        entries = Transaction.objects.filter(user=request.user)
        income = entries.filter(type="INCOME").aggregate(total=Sum("amount"))["total"] or 0
        expense = entries.filter(type="EXPENSE").aggregate(total=Sum("amount"))["total"] or 0
        context["budget_balance"] = income - expense
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