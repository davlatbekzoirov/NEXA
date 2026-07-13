from django.urls import path
from . import views

app_name = 'budget'
urlpatterns = [
    path('', views.budget_dashboard, name='budget'),
]