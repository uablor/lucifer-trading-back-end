# apps/user/presentation/api/v1/twofa_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.auth.application.use_cases.twofa.generate_qr import GenerateTwoFAUseCase
from apps.auth.application.use_cases.twofa.validate_setup import ValidateSetupTwoFAUseCase
from apps.auth.application.use_cases.twofa.validate_login import ValidateLoginTwoFAUseCase

class GenerateOTPView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        data = GenerateTwoFAUseCase().execute(request.user)
        return Response(data, status=201)


class ValidateOTPView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        otp = request.data.get("otp")
        if ValidateSetupTwoFAUseCase().execute(request.user, otp):
            return Response({"detail": "2FA enabled successfully"}, status=200)
        return Response({"detail": "Invalid OTP"}, status=400)


class ValidateOTP_UserLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny,]

    def post(self, request):
        otp = request.data.get("code")
        token = request.data.get("twoFALoginToken")
        email = request.data.get("email")

        jwt_token = ValidateLoginTwoFAUseCase().execute(email, otp, token)
        if jwt_token:
            return Response({"detail": "2FA verification successful", "token": jwt_token}, status=200)
        return Response({"detail": "Invalid OTP or token"}, status=400)
