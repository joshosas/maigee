import unittest
import pathlib

from app import app

basedir = pathlib.Path(__file__).parent.resolve()

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'test.db'}"
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_config(self):
        self.assertEqual(app.config["SQLALCHEMY_DATABASE_URI"], f"sqlite:///{basedir / 'test.db'}")
        self.assertEqual(app.config["SQLALCHEMY_TRACK_MODIFICATIONS"], False)

    def test_database(self):
        # Test adding a new row to the database.
        class Person(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(80), nullable=False)

        db.session.add(Person(name="Josh"))
        db.session.commit()

        # Test retrieving the row from the database.
        person = Person.query.filter_by(name="Josh").first()
        self.assertIsNotNone(person)
        self.assertEqual(person.name, "Josh")

    def test_marshmallow(self):
        # Test marshalling and unmarshalling a simple object.
        class PersonSchema(ma.Schema):
            class Meta:
                fields = ("id", "name")

        person_schema = PersonSchema()
        data = person_schema.dump({"id": 1, "name": "Josh"})
        self.assertEqual(data, {"id": 1, "name": "Josh"})

        person = person_schema.load(data)
        self.assertEqual(person["id"], 1)
        self.assertEqual(person["name"], "Josh")

if __name__ == "__main__":
    unittest.main()
