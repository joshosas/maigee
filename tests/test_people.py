import unittest
from unittest.mock import MagicMock, patch
from people import app, db, create, read_all, read_one, update, delete
from models import Person



class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_create(self):
        new_person = {'fname': 'John', 'lname': 'Doe'}
        response = self.app.post('/create', json=new_person)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'fname': 'John', 'lname': 'Doe', 'id': 1})

    def test_read_all(self):
        Person(fname='John', lname='Doe').save()
        Person(fname='Jane', lname='Doe').save()
        response = self.app.get('/read-all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_read_one(self):
        person = Person(fname='John', lname='Doe').save()
        response = self.app.get(f'/read-one/{person.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'fname': 'John', 'lname': 'Doe', 'id': person.id})

    def test_read_one_not_found(self):
        response = self.app.get('/read-one/1')
        self.assertEqual(response.status_code, 404)

    def test_update(self):
        person = Person(fname='John', lname='Doe').save()
        updated_person = {'fname': 'Jane', 'lname': 'Doe'}
        response = self.app.put(f'/update/{person.id}', json=updated_person)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'fname': 'Jane', 'lname': 'Doe', 'id': person.id})

    def test_update_not_found(self):
        response = self.app.put('/update/1', json={'fname': 'Jane', 'lname': 'Doe'})
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        person = Person(fname='John', lname='Doe').save()
        response = self.app.delete(f'/delete/{person.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'1 successfully deleted')

    def test_delete_not_found(self):
        response = self.app.delete('/delete/1')
        self.assertEqual(response.status_code, 404)
