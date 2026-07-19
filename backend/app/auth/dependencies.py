from typing import Annotated

from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.domain import User
from app.auth.login import LoginUser
from app.auth.passwords import PasswordHasher
from app.auth.persistence import SqlAlchemyUnitOfWork, SqlAlchemyUserRepository
from app.auth.registration import RegisterUser
from app.auth.tokens import get_access_token_user_id
from app.infrastructure.database import get_db_session
from app.infrastructure.settings import get_settings, Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_current_user(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_db_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = get_access_token_user_id(access_token, settings)
    if user_id is None:
        raise credentials_exception

    user = SqlAlchemyUserRepository(session).get_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user


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
