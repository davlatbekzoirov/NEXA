from django.urls import path
from . import views

app_name = 'roomieratio'
urlpatterns = [
    path('hub/', views.HouseholdHubView.as_view(), name='hub'),
    path('chore/<int:chore_id>/complete/', views.CompleteChoreView.as_view(), name='complete_chore'),
]