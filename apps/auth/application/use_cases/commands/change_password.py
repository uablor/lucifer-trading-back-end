from django.contrib.auth.hashers import make_password, check_password
from apps.user.application.use_cases.best_use_case import BestUserUseCase

class ChangePasswordUserCommand(BestUserUseCase):
    def __init__(self):
        super().__init__()

    def execute(self, data: dict, user_id: int):

        orm_obj = self.repo.get_by_id(user_id)
        if orm_obj is None:
            return None
        if not check_password(data['old_password'], orm_obj.password):
            raise ValueError("Old password is incorrect")

        new_password_hashed = make_password(data['new_password'])

        self.repo.change_password(orm_obj.id, new_password_hashed)
        return True

