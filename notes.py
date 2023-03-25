from flask import abort, make_response

from config import db
from models import Note, Person, note_schema


def read_one(note_id):
    """
    Retrieve a single note based on the note_id.
    
    Args:
    - note_id: The ID of the note to be retrieved.
    
    Returns:
    - If the note exists, returns the serialized version of the note.
    - If the note does not exist, returns a 404 error message.
    """
    note = Note.query.get(note_id)

    if note is not None:
        return note_schema.dump(note)
    else:
        abort(404, f"Note with ID {note_id} not found")



def update(note_id, note):
    """
    Update an existing note based on the note_id and the new content provided.
    
    Args:
    - note_id: The ID of the note to be updated.
    - note: The new content to be added to the note.
    
    Returns:
    - If the note exists, returns the serialized version of the updated note and a 201 status code.
    - If the note does not exist, returns a 404 error message.
    """
    existing_note = Note.query.get(note_id)

    if existing_note:
        update_note = note_schema.load(note, session=db.session)
        existing_note.content = update_note.content
        db.session.merge(existing_note)
        db.session.commit()
        return note_schema.dump(existing_note), 201
    else:
        abort(404, f"Note with ID {note_id} not found")


def delete(note_id):
    """
    Delete an existing note based on the note_id.
    
    Args:
    - note_id: The ID of the note to be deleted.
    
    Returns:
    - If the note exists, returns a 204 status code and a success message.
    - If the note does not exist, returns a 404 error message.
    """
    existing_note = Note.query.get(note_id)

    if existing_note:
        db.session.delete(existing_note)
        db.session.commit()
        return make_response(f"{note_id} successfully deleted", 204)
    else:
        abort(404, f"Note with ID {note_id} not found")


def create(note):
    """
    Create a new note based on the provided note data.
    
    Args:
    - note: The note data to be used to create the new note.
    
    Returns:
    - If the person exists, returns the serialized version of the new note and a 201 status code.
    - If the person does not exist, returns a 404 error message.
    """
    person_id = note.get("person_id")
    person = Person.query.get(person_id)

def create(note):
    person_id = note.get("person_id")
    person = Person.query.get(person_id)

    if person:
        new_note = note_schema.load(note, session=db.session)
        person.notes.append(new_note)
        db.session.commit()
        return note_schema.dump(new_note), 201
    else:
        abort(404, f"Person not found for ID: {person_id}")

