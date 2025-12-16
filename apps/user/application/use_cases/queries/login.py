
from apps.user.application.use_cases.best_use_case import BestUserUseCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from apps.user.infrastructure.mappers.user_mapper import UserMapper
from apps.user.domain.entities import User as DomainUser
from django.contrib.auth import authenticate
class LoginUserUseCase(BestUserUseCase):
    def __init__(self):
        super().__init__()

    def execute(self, email: str, password: str):
        user = authenticate(username=email, password=password)
        user_find = self.repo.get_by_email(email)
        if user is None:
            return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({"message": "User is not active"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # if not user_find.is_verify:
        #     return Response({"message": "User is not verified"}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)

        return {
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active ,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "is_superuser": user.is_superuser,
            "is_verify": user_find.is_verify,
            "is_2fa_enabled": user_find.is_2fa_enabled,
            "group": user_find.groups.first().name if user_find.groups else None
        }
