from typing import Protocol

from app.auth.repository import UserRepository


class UnitOfWork(Protocol):
    @property
    def users(self) -> UserRepository: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...
