'''File for setting up Flask application, initializing database'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import constants

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = constants.DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
database = SQLAlchemy(app)
CORS(app)
