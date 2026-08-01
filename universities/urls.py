from django.urls import path
from . import views
from .autocomplete import university_autocomplete

app_name = "universities"

urlpatterns = [
    path('', views.DashboardView.as_view(), name='main_uni'),

    path('universities/', views.UniversityListView.as_view(), name='university_list'),
    path('universities/add/', views.UniversityCreateView.as_view(), name='university_create'),
    path('universities/<int:pk>/', views.UniversityDetailView.as_view(), name='university_detail'),
    path('universities/<int:pk>/edit/', views.UniversityEditView.as_view(), name='university_edit'),
    path('universities/<int:pk>/delete/', views.UniversityDeleteView.as_view(), name='university_delete'),
    path('universities/<int:uni_pk>/scholarships/add/', views.ScholarshipCreateView.as_view(), name='scholarship_create'),

    path('universities/<int:uni_pk>/tasks/add/', views.TaskCreateView.as_view(), name='task_create'),
    path('universities/<int:uni_pk>/tasks/regenerate/', views.TaskRegenerateView.as_view(), name='task_regenerate'),
    path('tasks/<int:pk>/toggle/', views.TaskToggleView.as_view(), name='task_toggle'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),

    path('scholarships/', views.ScholarshipListView.as_view(), name='scholarship_list'),
    path('documents/', views.DocumentsView.as_view(), name='documents'),
    path('documents/<int:pk>/delete/', views.DocumentDeleteView.as_view(), name='document_delete'),
    path('scores/', views.ScoresView.as_view(), name='scores'),

    path('autocomplete/', university_autocomplete, name='university_autocomplete'),

    path('documents/<int:pk>/',                    views.DocumentDetailView.as_view(),          name='document_detail'),
    path('documents/<int:doc_pk>/versions/add/',   views.DocumentVersionUploadView.as_view(),  name='document_version_upload'),
    path('documents/versions/<int:pk>/delete/',    views.DocumentVersionDeleteView.as_view(),  name='document_version_delete'),
    path('documents/<int:doc_pk>/share/',          views.ShareLinkCreateView.as_view(),        name='share_link_create'),
    path('documents/share/<int:pk>/revoke/',       views.ShareLinkRevokeView.as_view(),        name='share_link_revoke'),
    path('shared/<uuid:token>/',                   views.SharedDocumentView.as_view(),     name='shared_document'),

    path('calendar/', views.CalendarFeedInfoView.as_view(), name='calendar_feed_info'),
    path('calendar/regenerate/', views.CalendarTokenRegenerateView.as_view(), name='calendar_token_regenerate'),
    path('calendar/<uuid:token>.ics', views.IcalFeedView.as_view(), name='ical_feed'),
]