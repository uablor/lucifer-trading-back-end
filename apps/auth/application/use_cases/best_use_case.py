from apps.auth.infrastructure.repositories.auth_repository import AuthRepository


class BestUserUseCase:
    def __init__(self):
        self.repo = AuthRepository()