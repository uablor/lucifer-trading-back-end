
from apps.user.infrastructure.repositories.user_repository import UserRepository
from rest_framework.response import Response
from rest_framework import status
from apps.user.application.use_cases.best_use_case import BestUserUseCase
from .get_email import GetEmailUserUseCase
from venv import logger
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class ForgotPasswordUserUseCase(BestUserUseCase):
    def __init__(self):
        super().__init__()
        self.repo_email = GetEmailUserUseCase()

    def execute(self, email: str):
        user = self.repo_email.execute(email)
        if not user:
            return None
        try:
            subject = 'Verify Your Email Address'
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = reverse("api:forgot-password", kwargs={"encoded_pk": encoded_pk, "token": token})
            reset_link = f"http://localhost:8000{reset_url}"
            subject = 'Password Reset Request'
            message = f'Hi {user.username},\n\nPlease click the link below to reset your password:\n\n{reset_link}'
            
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return {'message': 'Password reset email sent successfully'}
        except Exception as e:
            return {'message': 'Error sending password reset email'}

