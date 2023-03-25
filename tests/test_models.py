import unittest
from datetime import datetime

from config import db
from app import Note, Person, note_schema, person_schema, people_schema


class TestModels(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_note_model(self):
        note = Note(person_id=1, content="test note")
        db.session.add(note)
        db.session.commit()

        self.assertEqual(note.person_id, 1)
        self.assertEqual(note.content, "test note")
        self.assertIsInstance(note.timestamp, datetime)

    def test_person_model(self):
        person = Person(lname="Doe", fname="John")
        db.session.add(person)
        db.session.commit()

        note = Note(person_id=person.id, content="test note")
        db.session.add(note)
        db.session.commit()

        self.assertEqual(person.lname, "Doe")
        self.assertEqual(person.fname, "John")
        self.assertIsInstance(person.timestamp, datetime)
        self.assertEqual(person.notes[0].content, "test note")

    def test_note_schema(self):
        note = Note(person_id=1, content="test note")
        db.session.add(note)
        db.session.commit()

        data = note_schema.dump(note)

        self.assertEqual(data["person_id"], 1)
        self.assertEqual(data["content"], "test note")
        self.assertIsInstance(data["timestamp"], str)

    def test_person_schema(self):
        person = Person(lname="Doe", fname="John")
        db.session.add(person)
        db.session.commit()

        note = Note(person_id=person.id, content="test note")
        db.session.add(note)
        db.session.commit()

        data = person_schema.dump(person)

        self.assertEqual(data["lname"], "Doe")
        self.assertEqual(data["fname"], "John")
        self.assertIsInstance(data["timestamp"], str)
        self.assertEqual(data["notes"][0]["content"], "test note")

    def test_people_schema(self):
        person1 = Person(lname="Doe", fname="John")
        person2 = Person(lname="Smith", fname="Jane")
        db.session.add_all([person1, person2])
        db.session.commit()

        note1 = Note(person_id=person1.id, content="test note 1")
        note2 = Note(person_id=person2.id, content="test note 2")
        db.session.add_all([note1, note2])
        db.session.commit()

        data = people_schema.dump([person1, person2])

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["lname"], "Doe")
        self.assertEqual(data[1]["fname"], "Jane")
        self.assertIsInstance(data[0]["timestamp"], str)
        self.assertEqual(data[0]["notes"][0]["content"], "test note 1")
        self.assertEqual(data[1]["notes"][0]["content"], "test note 2")


if __name__ == "__main__":
    unittest.main()
