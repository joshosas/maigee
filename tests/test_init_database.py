import unittest
from datetime import datetime
from sqlalchemy.exc import OperationalError
from config import app, db
from models import Note, Person
from init_database import create_database, get_data_from_table, update_database

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

class TestNotes(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        with app.app_context():
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

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_data_from_table(self):
        with app.app_context():
            people = get_data_from_table(Person)
            notes = get_data_from_table(Note)
        self.assertEqual(len(people), 3)
        self.assertEqual(len(notes), 5)

    def test_create_database(self):
        with app.app_context():
            create_database(db)
            people = get_data_from_table(Person)
            notes = get_data_from_table(Note)
        self.assertEqual(len(people), 3)
        self.assertEqual(len(notes), 5)

    def test_update_database(self):
        with app.app_context():
            existing_people = get_data_from_table(Person)
            existing_notes = get_data_from_table(Note)
            update_database(db, existing_people, existing_notes)
            people = get_data_from_table(Person)
            notes = get_data_from_table(Note)
        self.assertEqual(len(people), 3)
        self.assertEqual(len(notes), 5)


if __name__ == '__main__':
    unittest.main()
