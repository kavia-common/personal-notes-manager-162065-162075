from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    """Response schema for JWT tokens."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Type of the token")


class TokenPayload(BaseModel):
    """Payload stored inside a JWT token."""
    sub: str = Field(..., description="Subject of the token, user email")
    exp: int = Field(..., description="Expiration timestamp")


class UserBase(BaseModel):
    """Base user info."""
    email: EmailStr = Field(..., description="User email")


class UserCreate(UserBase):
    """Payload for user registration."""
    password: str = Field(..., min_length=6, description="Plaintext password")


class UserLogin(UserBase):
    """Payload for user login."""
    password: str = Field(..., description="Plaintext password")


class UserOut(UserBase):
    """Response schema for user data."""
    id: int = Field(..., description="User ID")
