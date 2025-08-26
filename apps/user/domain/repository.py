# domain/repositories/book_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import User

class IUserRepository(ABC):

    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def save(self, book: User) -> User:
        pass

    @abstractmethod
    def update(self, book: User) -> User:
        pass

    @abstractmethod
    def soft_delete(self, book_id: int) -> None:
        pass
    
    @abstractmethod
    def hard_delete(self, book_id: int) -> None:
        pass
    @abstractmethod
    def verify_email(self, user_id: int) -> None:
        pass
    @abstractmethod
    def change_password(self,user_id: int, new_password_hashed: str) -> None:
        pass