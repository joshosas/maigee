from datetime import datetime

from marshmallow_sqlalchemy import fields
from config import db, ma


class Note(db.Model):
    """
    A model representing a note object.

    Attributes:
        id (int): The ID of the note.
        person_id (int): The ID of the person associated with the note.
        content (str): The content of the note.
        timestamp (datetime): The timestamp of when the note was created or updated.
    """
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class NoteSchema(ma.SQLAlchemyAutoSchema):
    """
    A schema for serializing and deserializing Note objects.

    Attributes:
        model (class): The Note model class.
        load_instance (bool): Whether to load instances of the model.
        sqla_session (Session): The SQLAlchemy session to use.
        include_fk (bool): Whether to include foreign keys.
    """
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Person(db.Model):
    """
    A model representing a person object.

    Attributes:
        id (int): The ID of the person.
        lname (str): The last name of the person.
        fname (str): The first name of the person.
        timestamp (datetime): The timestamp of when the person was created or updated.
        notes (relationship): A relationship to the person's notes.
    """
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), nullable=False)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    notes = db.relationship(
        Note,
        backref="person",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Note.timestamp)",
    )


class PersonSchema(ma.SQLAlchemyAutoSchema):
    """
    A schema for serializing and deserializing Person objects.

    Attributes:
        model (class): The Person model class.
        load_instance (bool): Whether to load instances of the model.
        sqla_session (Session): The SQLAlchemy session to use.
        include_relationships (bool): Whether to include relationships.
    """
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    notes = fields.Nested(NoteSchema, many=True)


note_schema = NoteSchema()
person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
