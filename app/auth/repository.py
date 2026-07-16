from typing import Protocol

from app.auth.domain import User


class UserRepository(Protocol):
    def create(self, email: str, password_hash: str) -> User: ...
