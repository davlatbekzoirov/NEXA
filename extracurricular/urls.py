from django.urls import path

from . import views

app_name = "extracurricular"

urlpatterns = [
    path("", views.CampusPulseView.as_view(), name="campuspulse"),

    path("clubs/", views.ClubListView.as_view(), name="club_list"),
    path("clubs/new/", views.ClubCreateView.as_view(), name="club_create"),
    path("clubs/<int:pk>/", views.ClubDetailView.as_view(), name="club_detail"),
    path("clubs/<int:pk>/edit/", views.ClubEditView.as_view(), name="club_edit"),
    path("clubs/<int:pk>/delete/", views.ClubDeleteView.as_view(), name="club_delete"),
    path("clubs/<int:pk>/roles/add/", views.ClubRoleAddView.as_view(), name="club_role_add"),
    path(
        "clubs/<int:pk>/roles/<int:role_pk>/delete/",
        views.ClubRoleDeleteView.as_view(),
        name="club_role_delete",
    ),

    path("volunteering/", views.VolunteerListView.as_view(), name="volunteer_list"),
    path("volunteering/new/", views.VolunteerCreateView.as_view(), name="volunteer_create"),
    path("volunteering/<int:pk>/edit/", views.VolunteerEditView.as_view(), name="volunteer_edit"),
    path("volunteering/<int:pk>/delete/", views.VolunteerDeleteView.as_view(), name="volunteer_delete"),

    path("impact/", views.ImpactListView.as_view(), name="impact_list"),
    path("impact/resume-generator/", views.ResumeGeneratorView.as_view(), name="resume_generator"),
    path("impact/new/", views.ImpactCreateView.as_view(), name="impact_create"),
    path("impact/<int:pk>/edit/", views.ImpactEditView.as_view(), name="impact_edit"),
    path("impact/<int:pk>/delete/", views.ImpactDeleteView.as_view(), name="impact_delete"),

    path("events/", views.EventListView.as_view(), name="event_list"),
    path("events/new/", views.EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/edit/", views.EventEditView.as_view(), name="event_edit"),
    path("events/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event_delete"),
    path("events/feed/regenerate/", views.RegenerateFeedTokenView.as_view(), name="regenerate_feed_token"),
    path("events/feed/<uuid:token>.ics", views.ICalFeedView.as_view(), name="ical_feed"),

    path("portfolio/settings/", views.PortfolioSettingsView.as_view(), name="portfolio_settings"),
    path("portfolio/<str:username>/", views.PublicPortfolioView.as_view(), name="public_portfolio"),

    path("analytics/insights/", views.AnalyticsInsightsView.as_view(), name="analytics_insights"),
]