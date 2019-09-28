from flask import app
from alayatodo import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from time import time

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), index=True, unique=True)
	password = db.Column(db.String(255))
	todos = db.relationship('Todo', backref='owner', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

	# # Improve security with password hash
	# def set_password(self, password):
	# 	self.password_hash = generate_password_hash(password)

	# def validate_password(self, password):
	# 	return check_password_hash(self.check_password_hash, password)

login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Todo #{}>'.format(self.id)