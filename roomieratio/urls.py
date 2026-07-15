from django.urls import path
from . import views

app_name = 'roomieratio'
urlpatterns = [
    path('hub/', views.household_hub, name='hub'),
    path('chore/<int:chore_id>/complete/', views.complete_chore, name='complete_chore'),
]