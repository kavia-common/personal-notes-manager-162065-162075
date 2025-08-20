from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base fields for a note."""
    title: str = Field(..., max_length=255, description="Title of the note")
    content: str = Field(..., description="Content of the note")


class NoteCreate(NoteBase):
    """Payload to create a new note."""
    pass


class NoteUpdate(BaseModel):
    """Payload to update a note."""
    title: Optional[str] = Field(None, max_length=255, description="Updated title")
    content: Optional[str] = Field(None, description="Updated content")


class NoteOut(NoteBase):
    """Response schema for note."""
    id: int = Field(..., description="Note ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last updated timestamp")
    owner_id: int = Field(..., description="Owner user ID")
