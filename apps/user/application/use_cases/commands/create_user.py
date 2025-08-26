from apps.user.infrastructure.repositories.user_repository import UserRepository
from apps.user.domain.entities import User as DomainUser
from apps.user.application.use_cases.best_use_case import BestUserUseCase

from django.contrib.auth.hashers import make_password
class CreateUserCommand(BestUserUseCase):
    def __init__(self):
        super().__init__()

    def execute(self, user: DomainUser, *args, **kwargs):
        
        user['password'] = make_password(user['password'])
        user = self.repo.save(user)
        return user
