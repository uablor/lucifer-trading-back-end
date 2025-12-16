from apps.user.infrastructure.repositories.user_repository import UserRepository
from apps.user.application.use_cases.best_use_case import BestUserUseCase
from apps.user.infrastructure.repositories.user_repository import UserRepository
from apps.user.application.use_cases.best_use_case import BestUserUseCase


class UpdateUserCommand(BestUserUseCase):
    def __init__(self):
        super().__init__()
        self.repo = UserRepository()

    def execute(self, newuser: dict, pk: int, *args, **kwargs):
        user_obj = self.repo.get_by_id(pk)
        if user_obj is None:
            return None

        newuser['id'] = user_obj.id  

        updated_user = self.repo.update(newuser, user_obj)
        return updated_user