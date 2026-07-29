from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/email/change/', views.EmailChangeRequestView.as_view(), name='email_change_request'),
    path('profile/email/confirm/', views.EmailChangeConfirmView.as_view(), name='email_change_confirm'),
    path('profile/password/', views.PasswordChangeView.as_view(), name='password_change'),
]