# domain/repositories/book_repository.py

from abc import ABC, abstractmethod

class IAuthRepository(ABC):
    @abstractmethod
    def verify_email(self, user_id: int) -> None:
        pass
    @abstractmethod
    def change_password(self,user_id: int, new_password_hashed: str) -> None:
        pass