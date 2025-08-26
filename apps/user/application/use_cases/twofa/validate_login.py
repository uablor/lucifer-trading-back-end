# apps/user/application/use_cases/twofa/validate_login.py
import jwt
from django.conf import settings
from django_otp.plugins.otp_totp.models import TOTPDevice
from apps.user.config.models import User
from apps.user.application.use_cases.best_use_case import BestUserUseCase

class ValidateLoginTwoFAUseCase(BestUserUseCase):
    
    def execute(self, email: str, otp: str, token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            email_user = payload.get("email")

            if email_user != email:
                return None

            user = self.repo.get_by_id(user_id)
            if not user:
                return None

            device = TOTPDevice.objects.get(user=user, name="default")

            if device.verify_token(otp):
                # ✅ คืน JWT token ของจริง
                real_token = jwt.encode(
                    {"user_id": user.id, "email": user.email},
                    settings.SECRET_KEY,
                    algorithm="HS256"
                )
                return real_token
            return None
        except Exception:
            return None
