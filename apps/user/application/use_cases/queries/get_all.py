
from apps.user.infrastructure.repositories.user_repository import UserRepository
from apps.user.application.use_cases.best_use_case import BestUserUseCase

class GetAllUserUseCase(BestUserUseCase):
    def __init__(self):
        super().__init__()
        
    def execute(self, **params):
        return self.repo.get_all(**params)
