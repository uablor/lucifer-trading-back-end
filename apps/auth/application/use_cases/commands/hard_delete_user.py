from apps.user.infrastructure.repositories.user_repository import UserRepository
from apps.user.domain.entities import User as DomainUser
from apps.user.application.use_cases.best_use_case import BestUserUseCase
from apps.user.application.use_cases.queries.get_one import GetOneUserUseCase

class HardDeleteUserCommand(BestUserUseCase):
    def __init__(self):
        super().__init__()
        self.get_by_id = GetOneUserUseCase()

    def execute(self, user_id: int):
        user = self.get_by_id.execute(user_id)
        if user is None:
            return None
        self.repo.hard_delete(user.id)
        return user

