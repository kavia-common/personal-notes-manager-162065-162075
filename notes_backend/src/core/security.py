from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import jwt
from passlib.context import CryptContext

from src.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# PUBLIC_INTERFACE
def get_password_hash(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


# PUBLIC_INTERFACE
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


# PUBLIC_INTERFACE
def create_access_token(subject: str, expires_delta_minutes: Optional[int] = None) -> str:
    """
    Create a JWT access token.

    Args:
        subject: The token subject (e.g., user id or email).
        expires_delta_minutes: Optional expiration in minutes; defaults to settings value.

    Returns:
        Encoded JWT string.
    """
    settings = get_settings()
    if expires_delta_minutes is None:
        expires_delta_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=expires_delta_minutes)
    to_encode: dict[str, Any] = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


# PUBLIC_INTERFACE
def decode_token(token: str) -> dict:
    """Decode a JWT token and return its payload."""
    settings = get_settings()
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
