from django.urls import path
from . import views

app_name = 'housing'
urlpatterns = [
    path('pipeline/', views.CrmPipelineView.as_view(), name='pipeline'),
    path('property/<int:pk>/move/<str:status>/', views.UpdateStatusView.as_view(), name='update_status'),
]