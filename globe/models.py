import os
from globe import app, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app.config.from_envvar('APP_CONFIG_FILE')

app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']



class User(db.Model):
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(30), unique=True)
	username = db.Column(db.String(30), unique=True)
	forename = db.Column(db.String(20))
	surname = db.Column(db.String(20))
	city = db.Column(db.String(40))
	followers = db.Column(db.String(6000))
	following = db.Column(db.String(6000))
	biography = db.Column(db.String(200))

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)


	def __init__(self, id, email, username, forename, city, followers, following, biography):
		self.id = id
		self.email=email
		self.username=username
		self.forename=forename
		self.surname=surname
		self.city=city
		self.followers=followers
		self.following=following
		self.biography=biography


	def __repr__(self):
		return '<Username %r>' % self.username


class UserAuth(db.Model):
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(30), unique=True)
	username = db.Column(db.String(30))
	registeredOn = db.Column(db.String(30))
	confirmationToken = db.Column(db.String(30))
	passwordToken = db.Column(db.String(30))
	lastLogin = db.Column(db.String(30))
	lastIPUsed = db.Column(db.String(15))
	verified = db.Column(db.Boolean)




	def __init__(self, id, email, username, registeredOn, confirmationToken, passwordToken, lastLogin, lastIPUsed, verified):
		self.id = id
		self.email = email
		self.username = username
		self.registeredOn = registeredOn
		self.confirmationToken = confirmationToken
		self.passwordToken = passwordToken
		self.lastLogin = lastLogin
		self.lastIPUsed = lastIPUsed
		self.verified = verified

	def __repr__(self):
		return '<User %r>' % self.username



class Post(db.Model):
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(30))
	postedOn = db.Column(db.String(30))
	postContent = db.Column(db.String(30))
	likes = db.Column(db.String(5))
	image = db.Column(db.String(30))
	city = db.Column(db.String(15))
	appreaciated = db.Column(db.Boolean)

	def __init__(self, id, email, username, postedOn, postContent, likes, image, city, appreaciated):
		self.id = id
		self.username=username
		self.postedOn = postedOn
		self.postContent = postContent
		self.likes = likes
		self.image = image
		self.city = city
		self.appreaciated = appreaciated


	def __repr__(self):
		return '<Id %r>' % self.id


class Admin(db.Model):
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(30), unique=True)
	username = db.Column(db.String(30))
	registeredOn = db.Column(db.String(30))
	confirmationToken = db.Column(db.String(30))
	passwordToken = db.Column(db.String(30))
	lastLogin = db.Column(db.String(30))
	lastIPUsed = db.Column(db.String(15))


	def __init__(self, id, email, username, registeredOn, confirmationToken, passwordToken, lastLogin, lastIPUsed):
		self.id = id
		self.email = email
		self.username = username
		self.registeredOn = registeredOn
		self.confirmationToken = confirmationToken
		self.passwordToken = passwordToken
		self.lastLogin = lastLogin
		self.lastIPUsed=lastIPUsed


	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<Username %r>' % self.username
