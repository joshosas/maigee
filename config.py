import pathlib

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

# Set the database URI to a SQLite file located in the same directory as this file.
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'people.db'}"

# Disable SQLAlchemy's modification tracking, which isn't needed in this simple app.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SQLAlchemy and Marshmallow objects.
db = SQLAlchemy(app)
ma = Marshmallow(app)
