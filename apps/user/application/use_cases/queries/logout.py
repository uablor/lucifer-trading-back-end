# apps/user/application/use_cases/commands/logout_user.py
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout as django_logout
class LogoutUserUseCase:
    def execute(self,request , refresh_token: str):
        django_logout(request)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return {"message": "Successfully logged out"}
        except Exception as e:
            return None
