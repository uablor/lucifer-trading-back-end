from apps.user.infrastructure.repositories.user_repository import UserRepository


class BestUserUseCase:
    def __init__(self):
        self.repo = UserRepository()