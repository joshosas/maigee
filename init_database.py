from datetime import datetime
from sqlalchemy.exc import OperationalError

from config import app, db
from models import Note, Person

PEOPLE_NOTES = [
    {
        "lname": "Fairy",
        "fname": "Tooth",
        "notes": [
            ("I brush my teeth after each meal.", "2022-01-06 17:10:24"),
            (
                "The other day a friend said, I have big teeth.",
                "2022-03-05 22:17:54",
            ),
            ("Do you pay per gram?", "2022-03-05 22:18:10"),
        ],
    },
    {
        "lname": "Ruprecht",
        "fname": "Knecht",
        "notes": [
            (
                "I swear, I'll do better this year.",
                "2022-01-01 09:15:03",
            ),
            (
                "Really! Only good deeds from now on!",
                "2022-02-06 13:09:21",
            ),
        ],
    },
    {
        "lname": "Bunny",
        "fname": "Easter",
        "notes": [
            (
                "Please keep the current inflation rate in mind!",
                "2022-01-07 22:47:54",
            ),
            ("No need to hide the eggs this time.", "2022-04-06 13:03:17"),
        ],
    },
]


def get_data_from_table(model):
    """
    Queries the database for all entries of the given model.

    Args:
        model: The SQLAlchemy model to query.

    Returns:
        A list of entries from the given table, or an empty list if there was an error.
    """
    try:
        data = db.session.query(model).all()
        db.session.close()
        return data
    except OperationalError:
        return []


def create_database(db):
    """
    Creates a new database using the data in the PEOPLE_NOTES list.

    Args:
        db: The SQLAlchemy database object to use.
    """
    db.create_all()
    for data in PEOPLE_NOTES:
        new_person = Person(lname=data.get("lname"), fname=data.get("fname"))
        for content, timestamp in data.get("notes", []):
            new_person.notes.append(
                Note(
                    content=content,
                    timestamp=datetime.strptime(
                        timestamp, "%Y-%m-%d %H:%M:%S"
                    ),
                )
            )
        db.session.add(new_person)
    db.session.commit()
    print("Created new database")


def update_database(db, existing_people, existing_notes):
    """
    Updates an existing database with new data.

    Args:
        db: The SQLAlchemy database object to use.
        existing_people: A list of Person objects already in the database.
        existing_notes: A list of Note objects already in the database.
    """
    db.drop_all()
    db.create_all()
    for person in existing_people:
        db.session.merge(person)
    for note in existing_notes:
        db.session.merge(note)
    db.session.commit()
    print("Updated existing database")


with app.app_context():
    existing_people = get_data_from_table(Person)
    existing_notes = get_data_from_table(Note)

    if not existing_people:
        create_database(db)
    else:
        update_database(db, existing_people, existing_notes
