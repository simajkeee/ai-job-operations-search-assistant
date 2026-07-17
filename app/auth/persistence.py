from datetime import datetime
from uuid import UUID, uuid4

from psycopg.errors import UniqueViolation
from sqlalchemy import String, DateTime, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID

from app.auth.domain import User
from app.auth.errors import EmailAlreadyRegisteredError
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
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, email: str, password_hash: str) -> User:
        user = UserModel(
            email=email,
            password_hash=password_hash,
        )

        self._session.add(user)

        try:
            self._session.flush()
        except IntegrityError as error:
            if isinstance(error.orig, UniqueViolation):
                raise EmailAlreadyRegisteredError() from error
            raise

        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
        )

    def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email)
        user: UserModel | None = self._session.scalars(statement).one_or_none()

        if user is None:
            return None

        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
        )


class SqlAlchemyUnitOfWork:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._users = SqlAlchemyUserRepository(self._session)

    @property
    def users(self) -> UserRepository:
        return self._users

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
