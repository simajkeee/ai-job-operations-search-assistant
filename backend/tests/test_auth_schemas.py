import pytest
from pydantic import ValidationError

from app.auth.schemas import RegisterUserRequest


@pytest.mark.parametrize(
    "password",
    ["short-password", "x" * 129],
)
def test_register_request_rejects_invalid_passwords(password: str) -> None:
    with pytest.raises(ValidationError):
        RegisterUserRequest(email="test@mail.com", password=password)
