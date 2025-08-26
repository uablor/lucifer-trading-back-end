
from apps.user.application.use_cases.best_use_case import BestUserUseCase
from apps.user.application.use_cases.queries.get_one import GetOneUserUseCase

class SoftDeleteUserCommand(BestUserUseCase):
    def __init__(self):
        super().__init__()
        self.get_by_id = GetOneUserUseCase()

    def execute(self, user_id: int):
        
        user = self.get_by_id.execute(user_id)
        if user is None:
            return None
        self.repo.soft_delete(user.id)
        return user

