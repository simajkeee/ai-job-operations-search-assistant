from typing import Protocol
from uuid import UUID

from app.auth.domain import User


class UserRepository(Protocol):
    def create(self, email: str, password_hash: str) -> User: ...

    def get_by_email(self, email: str) -> User | None: ...

    def get_by_id(self, user_id: UUID) -> User | None: ...
