from django.urls import path
from . import views

app_name = 'housing'
urlpatterns = [
    path('pipeline/', views.crm_pipeline, name='pipeline'),
    path('property/<int:pk>/move/<str:status>/', views.update_status, name='update_status'),
]