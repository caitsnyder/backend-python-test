from flask import app
from alayatodo import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), index=True, unique=True)
	password = db.Column(db.String(255))

	def __repr__(self):
		return '<User {}>'.format(self.username)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Todo #{}>'.format(self.id)