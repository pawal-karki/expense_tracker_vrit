from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView,
    UserLoginView,
    logout_view,
    user_profile_view,
    verify_email_view,
    resend_email_verification_view,
    email_confirm_redirect,
    account_email_verification_sent_view
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='rest_register'),
    path('login/', UserLoginView.as_view(), name='rest_login'),
    path('logout/', logout_view, name='rest_logout'),
    path('refresh/', TokenRefreshView.as_view(), name='rest_refresh'),
    path('profile/', user_profile_view, name='rest_profile'),
    path('verify-email/', verify_email_view, name='rest_verify_email'),
    path('resend-email/', resend_email_verification_view, name='rest_resend_email'),
    path('account-confirm-email/<str:key>/', email_confirm_redirect, name='account_confirm_email'),
    path('account-email-verification-sent/', account_email_verification_sent_view, name='account_email_verification_sent'),
] 