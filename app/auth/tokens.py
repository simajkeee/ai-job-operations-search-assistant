from datetime import datetime, timezone, timedelta
from uuid import UUID

import jwt

from app.infrastructure.settings import Settings


def create_access_token(user_id: UUID, settings: Settings) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes,
    )

    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": expires_at,
        },
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )
