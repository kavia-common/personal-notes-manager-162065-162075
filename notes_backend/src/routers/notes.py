from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.api.deps import get_current_user, get_db
from src.db.models import Note, User
from src.schemas.notes import NoteCreate, NoteOut, NoteUpdate

router = APIRouter()


@router.get(
    "",
    response_model=List[NoteOut],
    summary="List notes",
    description="List notes for the current user with optional search, pagination, and sorting.",
)
# PUBLIC_INTERFACE
def list_notes(
    q: Optional[str] = Query(default=None, description="Search text to match in title or content"),
    skip: int = Query(default=0, ge=0, description="Items to skip"),
    limit: int = Query(default=20, ge=1, le=100, description="Max number of items to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[NoteOut]:
    """
    List notes owned by the current user with optional search and pagination.
    """
    query = db.query(Note).filter(Note.owner_id == current_user.id)
    if q:
        like_str = f"%{q}%"
        query = query.filter(or_(Note.title.ilike(like_str), Note.content.ilike(like_str)))
    query = query.order_by(Note.updated_at.desc())
    notes = query.offset(skip).limit(limit).all()
    return [NoteOut.model_validate(n.__dict__) | {"owner_id": n.owner_id} for n in notes]  # type: ignore


@router.post(
    "",
    response_model=NoteOut,
    status_code=201,
    summary="Create a note",
    description="Create a new note for the current user.",
)
# PUBLIC_INTERFACE
def create_note(
    payload: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NoteOut:
    """
    Create a new note for the current user.
    """
    note = Note(title=payload.title, content=payload.content, owner_id=current_user.id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return NoteOut(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        updated_at=note.updated_at,
        owner_id=note.owner_id,
    )


@router.get(
    "/{note_id}",
    response_model=NoteOut,
    summary="Get a note",
    description="Retrieve a single note by ID for the current user.",
    responses={404: {"description": "Note not found"}},
)
# PUBLIC_INTERFACE
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NoteOut:
    """
    Get a note by ID belonging to the current user.
    """
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteOut(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        updated_at=note.updated_at,
        owner_id=note.owner_id,
    )


@router.put(
    "/{note_id}",
    response_model=NoteOut,
    summary="Update a note",
    description="Update an existing note fields for the current user.",
    responses={404: {"description": "Note not found"}},
)
# PUBLIC_INTERFACE
def update_note(
    note_id: int,
    payload: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NoteOut:
    """
    Update a note by ID for the current user.
    """
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content

    db.add(note)
    db.commit()
    db.refresh(note)
    return NoteOut(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        updated_at=note.updated_at,
        owner_id=note.owner_id,
    )


@router.delete(
    "/{note_id}",
    status_code=204,
    summary="Delete a note",
    description="Delete a note by ID for the current user.",
    responses={404: {"description": "Note not found"}},
)
# PUBLIC_INTERFACE
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete a note by ID belonging to the current user.
    """
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    db.delete(note)
    db.commit()
    return None
