import sqlite3
import os
from flask import Flask, g
from flask_login import LoginManager

# Get SQLALCHEMY for ORM
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Get configuration settings
from config import Config

# Moved global vars to dotenv file for security
SECRET_KEY = os.environ.get('SECRET_KEY') # Why is this not being imported via 'from config import Config'?

app = Flask(__name__)
app.config.from_object(Config)

# Assign variables for ORM mapping use
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


# Commented out below and enabled SQLAlchemy and Migrate instead
# def connect_db():
#     conn = sqlite3.connect(os.environ.get('DATABASE'))
#     conn.row_factory = sqlite3.Row
#     return conn


# @app.before_request
# def before_request():
#     g.db = connect_db()


# @app.teardown_request
# def teardown_request(exception):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close()



from alayatodo import views, models