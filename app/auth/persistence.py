from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID

from app.auth.domain import User
from app.auth.repository import UserRepository
from app.infrastructure.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class SqlAlchemyUserRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, email: str, password_hash: str) -> User:
        user = UserModel(
            email=email,
            password_hash=password_hash,
        )

        self._session.add(user)
        self._session.flush()

        return User(user.id, user.email, user.created_at)


class SqlAlchemyUnitOfWork:
    def __init__(self, session: Session):
        self._session = session
        self._users = SqlAlchemyUserRepository(self._session)

    @property
    def users(self) -> UserRepository:
        return self._users

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
