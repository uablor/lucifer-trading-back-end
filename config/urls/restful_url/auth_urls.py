from django.urls import path
from apps.user.presentation.api.views.auth_view import (
    UserAuthMeView,
    UserLoginView,
    UserLogoutView,
    VerifyEmailAPIView,
    PasswordResetView,
    ChangePasswordView,
    ForgotPasswordView,
    ResendVerifyEmailAPIView,
    )

from rest_framework.routers import DefaultRouter


router = DefaultRouter()


urlpatterns = [

    path('me/', UserAuthMeView.as_view(), name='user-auth-me'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('resend-verify-email/', ResendVerifyEmailAPIView.as_view(), name='resend-verify-email'),
    
    

    
]

urlpatterns += router.urls