import os, sys


from globe import app, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy as sa
from sqlalchemy import Column, Integer, String, DateTime, Unicode, ForeignKey, Sequence, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import PasswordType, IPAddressType, EncryptedType, URLType, JSONType

app.config.from_envvar('APP_CONFIG_FILE')
secret_key = os.environ['APP_SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']


class User(db.Model):
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(60), unique=True)
	username = db.Column(db.String(60), unique=True)
	password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
        ]
	))
	confirmationToken = db.Column(db.String())
	passwordToken = db.Column(db.String())
	forename = db.Column(db.String(20))
	surname = db.Column(db.String(20))
	city = db.Column(db.String(40))
	followers = db.Column(db.String(6000))
	following = db.Column(db.String(6000))
	biography = db.Column(db.String(200))
	verified = db.Column(db.Boolean)


	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)


	def __init__(self, id, email, username, password, forename, surname, city, followers, following, biography, confirmationToken, passwordToken, verified):
		self.id = id
		self.email=email
		self.username=username
		self.password=password
		self.forename=forename
		self.surname=surname
		self.city=city
		self.followers=followers
		self.following=following
		self.biography=biography
		self.confirmationToken=confirmationToken
		self.passwordToken=passwordToken
		self.verified=verified


	def __repr__(self):
		return '<Username %r>' % self.username



class Post(db.Model):
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(60))
	postedOn = db.Column(db.String(60))
	postContent = db.Column(db.String(60))
	likes = db.Column(db.String(5))
	image = db.Column(db.String(250))
	city = db.Column(db.String(15))
	coordinates = db.Column(db.String)
	appreaciated = db.Column(db.Boolean)
	isPanorama = db.Column(db.Boolean)

	def __init__(self, id, username, postedOn, postContent, likes, image, city, coordinates, appreaciated, isPanorama):
		self.id = id
		self.username=username
		self.postedOn = postedOn
		self.postContent = postContent
		self.likes = likes
		self.image = image
		self.city = city
		self.coordinates = coordinates
		self.appreaciated = appreaciated
		self.isPanorama = isPanorama


	def __repr__(self):
		return '<Id %r>' % self.id


#no time to create an admin panel for now
'''class Admin(db.Model):
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(60), unique=True)
	username = db.Column(db.String(60))
	registeredOn = db.Column(db.String(60))
	confirmationToken = db.Column(db.String(60))
	passwordToken = db.Column(db.String(60))
	lastLogin = db.Column(db.String(60))
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
'''
