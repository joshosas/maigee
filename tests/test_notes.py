import unittest
from app import app
from models import Note, Person
from config import db
from flask import json


class TestNoteAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_read_one(self):
        # create a note
        person = Person(name="Test Person")
        note = Note(title="Test Note", content="Test Content", person=person)
        db.session.add(note)
        db.session.commit()

        # send GET request to retrieve the note
        response = self.app.get(f"/note/{note.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["title"], "Test Note")
        self.assertEqual(response.json["content"], "Test Content")
        self.assertEqual(response.json["person"]["name"], "Test Person")

        # send GET request to retrieve a non-existent note
        response = self.app.get("/note/100")
        self.assertEqual(response.status_code, 404)

    def test_update(self):
        # create a note
        person = Person(name="Test Person")
        note = Note(title="Test Note", content="Test Content", person=person)
        db.session.add(note)
        db.session.commit()

        # send PUT request to update the note
        update_data = {"title": "New Title", "content": "New Content"}
        response = self.app.put(f"/note/{note.id}", json=update_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["title"], "New Title")
        self.assertEqual(response.json["content"], "New Content")

        # send PUT request to update a non-existent note
        response = self.app.put("/note/100", json=update_data)
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        # create a note
        person = Person(name="Test Person")
        note = Note(title="Test Note", content="Test Content", person=person)
        db.session.add(note)
        db.session.commit()

        # send DELETE request to delete the note
        response = self.app.delete(f"/note/{note.id}")
        self.assertEqual(response.status_code, 204)

        # make sure the note was deleted
        note = Note.query.get(note.id)
        self.assertIsNone(note)

        # send DELETE request to delete a non-existent note
        response = self.app.delete("/note/100")
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        # create a person
        person = Person(name="Test Person")
        db.session.add(person)
        db.session.commit()

        # send POST request to create a new note
        new_note_data = {"title": "New Note", "content": "New Content", "person_id": person.id}
        response = self.app.post("/note", json=new_note_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["title"], "New Note")
        self.assertEqual(response.json["content"], "New Content")
        self.assertEqual(response.json["person"]["name"], "Test Person")

        # send POST request to create a new note with invalid person_id
        new_note_data = {"title": "New Note", "content": "New Content", "person_id": 100}
        response = self.app.post("/note", json=new_note_data)
        self.assertEqual(response.status_code, 404)
