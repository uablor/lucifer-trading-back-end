from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from apps.user.application.use_cases.best_use_case import BestUserUseCase

class PasswordResetCommand(BestUserUseCase):
    def __init__(self):
        super().__init__()

    def execute(self, data: dict, encoded_pk: str, token: str):
        try:
            user_id = force_str(urlsafe_base64_decode(encoded_pk))
            user = self.repo.get_by_id(user_id)
        except Exception:
            raise ValueError("Invalid reset link")

        if user is None or not default_token_generator.check_token(user, token):
            raise ValueError("Invalid or expired token")

        new_password_hashed = make_password(data['new_password'])
        self.repo.change_password(user.id, new_password_hashed)
        return {"message": "Password has been reset successfully"}

