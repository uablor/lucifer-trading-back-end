
from apps.user.application.use_cases.best_use_case import BestUserUseCase
from apps.user.application.use_cases.queries.get_one import GetOneUserUseCase
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

class VerifyEmailCommand(BestUserUseCase):
    def __init__(self):
        super().__init__()
        self.get_by_id = GetOneUserUseCase()

    def execute(self, uid: str, token: str):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = self.get_by_id.execute(uid)
        except (TypeError, ValueError, OverflowError):
            return None

        if user is not None and default_token_generator.check_token(user, token):
            self.repo.verify_email(user.id)
            return user
        return None

