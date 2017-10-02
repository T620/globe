from globe import app, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class User(db.Model):
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(30), unique=True)
	username = db.Column(db.String(30), unique=True)
	forename = db.Column(db.String(20))
	surname = db.Column(db.String(20))
	city = db.Column(db.String(40))
	followers = db.Column(db.Text(6000))
	following = db.Column(db.Text(6000))
	biography = db.Column(db.Text(200))

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)


	def __init__(self, id, email, username, password, reset_key, confirmation_token, verified):
		self.id = id
		self.email=email
		self.username=username
		self.password=password
		self.reset_key=reset_key
		self.confirmation_token=confirmation_token
		self.verified=verified

	def __repr__(self):
		return '<Name %r>' % self.username


class UserAut(db.Model):
	

class Roster(db.Model):
	__table_args__ = {'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	member_type = db.Column(db.String(20))
	name = db.Column(db.String(80), unique=True)

	def __init__(self, id, name, member_type):
		self.id = id
		self.name = name
		self.member_type = member_type

	def __repr__(self):
		return '<Name %r>' % self.name


class Events(db.Model):
	__table_args__ = {'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(80))
	img = db.Column(db.String(120))
	post = db.Column(db.String(2000))

	def __init__(self, id, title, img, post):
		self.id = id
		self.title = title
		self.img = img
		self.post = post

	def __repr__(self):
		return '<Title %r>' % self.title


class Testimonials(db.Model):
		__table_args__ = {'extend_existing': True}
		id = db.Column(db.Integer, primary_key=True, autoincrement=True)
		name = db.Column(db.String(40))
		content = db.Column(db.String(200))

		def __init__(self, id, name, content):
			self.id = id
			self.name = name
			self.content = content

		def __repr__(self):
			return '<Comment %r>' % self.content


class Gallery(db.Model):
		__table_args__ = {'extend_existing': True}
		id = db.Column(db.Integer, primary_key=True, autoincrement=True)
		img = db.Column(db.String(200))
		comment = db.Column(db.String(200))

		def __init__(self, id, img, comment):
			self.id = id
			self.img = img
			self.comment = comment

		def __repr__(self):
			return '<Image %r>' % self.img
