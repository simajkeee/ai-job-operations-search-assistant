from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from app.auth.dependencies import get_register_user
from app.auth.errors import EmailAlreadyRegisteredError
from app.auth.registration import RegisterUser
from app.auth.schemas import RegisterUserRequest, RegisterUserResponse

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


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
