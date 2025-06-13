from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4, UUID

app = FastAPI(title="Notes CRUD API")


notes_db = {}


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: UUID


@app.post("/notes/", response_model=Note)
def create_note(note: NoteCreate):
    note_id = uuid4()
    new_note = Note(id=note_id, **note.dict())
    notes_db[note_id] = new_note
    return new_note

# Get all notes
@app.get("/notes/", response_model=List[Note])
def get_notes():
    return list(notes_db.values())

# Get a note by ID
@app.get("/notes/{note_id}", response_model=Note)
def get_a_note(note_id: UUID):
    if note_id in notes_db:
        return notes_db[note_id]
    raise HTTPException(status_code=404, detail="Note not found")

# Update a note
@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: UUID, updated_note: NoteCreate):
    if note_id in notes_db:
        updated = Note(id=note_id, **updated_note.dict())
        notes_db[note_id] = updated
        return updated
    raise HTTPException(status_code=404, detail="Note not found")

# Delete a note
@app.delete("/notes/{note_id}")
def delete_note(note_id: UUID):
    if note_id in notes_db:
        del notes_db[note_id]
        return {"detail": "Note deleted"}
    raise HTTPException(status_code=404, detail="Note not found")
