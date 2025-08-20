from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.core.security import decode_token
from src.db.models import User
from src.db.session import get_session_factory

# OAuth2 bearer token dependency. tokenUrl should match the login route.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """
    Dependency that yields a SQLAlchemy session and ensures it's closed afterwards.
    """
    SessionLocal = get_session_factory()
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PUBLIC_INTERFACE
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Extract current user from Bearer token.

    Raises:
        HTTPException: 401 if token invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        email: Optional[str] = payload.get("sub")
    except Exception:
        raise credentials_exception

    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user
