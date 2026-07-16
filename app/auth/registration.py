from app.auth.domain import User
from app.auth.passwords import PasswordHasher
from app.auth.unit_of_work import UnitOfWork


class RegisterUser:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        password_hasher: PasswordHasher,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._password_hasher = password_hasher

    def execute(self, email: str, password: str) -> User:
        password_hash = self._password_hasher.hash(password)

        try:
            user = self._unit_of_work.users.create(
                email=email,
                password_hash=password_hash,
            )
            self._unit_of_work.commit()
        except Exception:
            self._unit_of_work.rollback()
            raise

        return user
