from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("features/", views.features, name="features"),
    path("help/", views.help_page, name="help"),
    path("contact/", views.contact, name="contact"),
]