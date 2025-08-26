
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

class ResendVerifyEmailUserUseCase(BestUserUseCase):
    def __init__(self):
        super().__init__()
        self.repo_email = GetEmailUserUseCase()

    def execute(self, email: str):
        user = self.repo_email.execute(email)
        if not user:
            return None
        if user.is_verify:
            return {'message': 'this email is already verified'}
        try:
            subject = 'Verify Your Email Address'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            verify_url = f"http://localhost:8000{reverse('api:verify-email')}?uid={uid}&token={token}"
            context = {
                'user': user,
                'verify_url': verify_url,
            }
            convert_to_html_content =  render_to_string(
            template_name="verification_email.html",
            context = context
            )
            
            plain_message = strip_tags(convert_to_html_content)
            a = send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=convert_to_html_content,
            fail_silently=True,
            ) 
            return {'message': 'Verification email sent successfully'}
        except Exception as e:
            return {'message': 'Failed to send verification email'}

