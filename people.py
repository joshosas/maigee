from flask import abort, make_response
from config import db
from models import Person, people_schema, person_schema


def read_all():
    """
    Retrieve all people in the database.

    Returns:
        A JSON representation of all people in the database.
    """
    people = Person.query.all()
    return people_schema.dump(people)


def create(person):
    """
    Create a new person.

    Args:
        person: A dictionary containing the information for the new person.

    Returns:
        A JSON representation of the newly created person.
    """
    new_person = person_schema.load(person, session=db.session)
    db.session.add(new_person)
    db.session.commit()
    return person_schema.dump(new_person), 201


def read_one(person_id):
    """
    Retrieve a single person by their ID.

    Args:
        person_id: The ID of the person to retrieve.

    Returns:
        A JSON representation of the requested person.

    Raises:
        404 error: If the person with the given ID does not exist.
    """
    person = Person.query.get(person_id)

    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Person with ID {person_id} not found")


def update(person_id, person):
    """
    Update an existing person.

    Args:
        person_id: The ID of the person to update.
        person: A dictionary containing the updated information for the person.

    Returns:
        A JSON representation of the updated person.

    Raises:
        404 error: If the person with the given ID does not exist.
    """
    existing_person = Person.query.get(person_id)

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        existing_person.lname = update_person.lname
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person), 201
    else:
        abort(404, f"Person with ID {person_id} not found")


def delete(person_id):
    """
    Delete an existing person.

    Args:
        person_id: The ID of the person to delete.

    Returns:
        A success message if the person was successfully deleted.

    Raises:
        404 error: If the person with the given ID does not exist.
    """
    existing_person = Person.query.get(person_id)

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{person_id} successfully deleted", 200)
    else:
        abort(404, f"Person with ID {person_id} not found")
