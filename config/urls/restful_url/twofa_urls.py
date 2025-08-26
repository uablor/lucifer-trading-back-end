from django.urls import path
from apps.user.presentation.api.views.twofa_views import (
    GenerateOTPView,
    ValidateOTPView,
    ValidateOTP_UserLoginView
    )

from rest_framework.routers import DefaultRouter


router = DefaultRouter()


urlpatterns = [

    path('generate-otp/', GenerateOTPView.as_view(), name='generate-otp'),
    path('validate-otp/', ValidateOTPView.as_view(), name='validate-otp'),
    path('validate-otp-user-login/', ValidateOTP_UserLoginView.as_view(), name='validate-otp-user-login'),

]

urlpatterns += router.urls