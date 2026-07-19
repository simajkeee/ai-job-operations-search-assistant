from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependencies import get_register_user, get_login_user, get_current_user
from app.auth.domain import User
from app.auth.errors import EmailAlreadyRegisteredError, InvalidCredentialsError
from app.auth.login import LoginUser
from app.auth.registration import RegisterUser
from app.auth.schemas import (
    RegisterUserRequest,
    RegisterUserResponse,
    AccessTokenResponse,
    UserResponse,
)
from app.auth.tokens import create_access_token
from app.infrastructure.settings import Settings, get_settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=RegisterUserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterUserRequest,
    register_user: Annotated[RegisterUser, Depends(get_register_user)],
) -> RegisterUserResponse:
    try:
        user = register_user.execute(
            email=request.email,
            password=request.password,
        )
    except EmailAlreadyRegisteredError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        ) from error

    return RegisterUserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
    )


@router.post("/token", response_model=AccessTokenResponse)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_user: Annotated[LoginUser, Depends(get_login_user)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AccessTokenResponse:
    try:
        user = login_user.execute(
            email=form_data.username,
            password=form_data.password,
        )
    except InvalidCredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    return AccessTokenResponse(
        access_token=create_access_token(user.id, settings),
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at,
    )
