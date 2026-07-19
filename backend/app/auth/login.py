from app.auth.domain import User
from app.auth.errors import InvalidCredentialsError
from app.auth.passwords import PasswordHasher
from app.auth.repository import UserRepository


class LoginUser:
    def __init__(self, users: UserRepository, password_hasher: PasswordHasher) -> None:
        self._users = users
        self._password_hasher = password_hasher

    def execute(self, email: str, password: str) -> User:
        user = self._users.get_by_email(email)

        if user is None or not self._password_hasher.verify(
            password, user.password_hash
        ):
            raise InvalidCredentialsError()

        return user
