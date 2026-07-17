from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.auth.login import LoginUser
from app.auth.passwords import PasswordHasher
from app.auth.persistence import SqlAlchemyUnitOfWork, SqlAlchemyUserRepository
from app.auth.registration import RegisterUser
from app.infrastructure.database import get_db_session


def get_register_user(
    session: Annotated[Session, Depends(get_db_session)],
) -> RegisterUser:
    return RegisterUser(
        unit_of_work=SqlAlchemyUnitOfWork(session),
        password_hasher=PasswordHasher(),
    )


def get_login_user(
    session: Annotated[Session, Depends(get_db_session)],
) -> LoginUser:
    return LoginUser(
        users=SqlAlchemyUserRepository(session),
        password_hasher=PasswordHasher(),
    )
