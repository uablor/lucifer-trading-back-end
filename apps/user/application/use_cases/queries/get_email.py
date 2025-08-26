
from apps.user.infrastructure.repositories.user_repository import UserRepository
from rest_framework.response import Response
from rest_framework import status
from apps.user.application.use_cases.best_use_case import BestUserUseCase

class GetEmailUserUseCase(BestUserUseCase):
    def __init__(self):
        super().__init__()

    def execute(self, email: str):
        user = self.repo.get_by_email(email)
        return user

