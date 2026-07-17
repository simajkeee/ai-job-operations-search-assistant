from datetime import datetime, timezone
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.auth.domain import User
from app.auth.errors import EmailAlreadyRegisteredError
from app.auth.passwords import PasswordHasher
from app.auth.registration import RegisterUser
from app.auth.repository import UserRepository
from app.auth.unit_of_work import UnitOfWork


def test_registration_creates_user_with_hashed_password() -> None:
    repository_mock = Mock(spec=UserRepository)
    unit_of_work_mock = Mock(spec=UnitOfWork)
    unit_of_work_mock.users = repository_mock
    password_hasher = Mock(spec=PasswordHasher)

    email = "test@mail.com"
    plaintext_password = "plain-password"
    password_hash = "hashed-password"
    user = User(
        id=uuid4(),
        email=email,
        password_hash=password_hash,
        created_at=datetime.now(timezone.utc),
    )
    unit_of_work_mock.users.create.return_value = user
    password_hasher.hash.return_value = password_hash

    register_user = RegisterUser(
        unit_of_work=unit_of_work_mock,
        password_hasher=password_hasher,
    )

    result = register_user.execute(email=email, password=plaintext_password)

    password_hasher.hash.assert_called_once_with(plaintext_password)
    repository_mock.create.assert_called_once_with(
        email=email, password_hash=password_hash
    )
    unit_of_work_mock.commit.assert_called_once()
    unit_of_work_mock.rollback.assert_not_called()
    assert result == user


def test_registration_rolls_back_when_email_is_registered() -> None:
    repository_mock = Mock(spec=UserRepository)
    unit_of_work_mock = Mock(spec=UnitOfWork)
    unit_of_work_mock.users = repository_mock
    password_hasher = Mock(spec=PasswordHasher)

    error = EmailAlreadyRegisteredError()
    repository_mock.create.side_effect = error
    password_hasher.hash.return_value = "hashed-password"

    register_user = RegisterUser(
        unit_of_work=unit_of_work_mock,
        password_hasher=password_hasher,
    )

    with pytest.raises(EmailAlreadyRegisteredError) as exception_info:
        register_user.execute(
            email="test@mail.com",
            password="plain-password",
        )

    assert exception_info.value is error
    unit_of_work_mock.rollback.assert_called_once()
    unit_of_work_mock.commit.assert_not_called()
