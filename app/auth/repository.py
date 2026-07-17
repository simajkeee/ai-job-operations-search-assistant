from typing import Protocol

from app.auth.domain import User


class UserRepository(Protocol):
    def create(self, email: str, password_hash: str) -> User: ...

    def get_by_email(self, email: str) -> User | None: ...
