from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render


def home(request):
    return render(request, "home/index.html")


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
