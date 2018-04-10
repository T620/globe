import os, sys
from globe import app, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy as sa
from sqlalchemy import Column, Integer, String, DateTime, Unicode, ForeignKey, Sequence, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import PasswordType, IPAddressType, EncryptedType, URLType
from sqlalchemy.dialects.postgresql import JSON
#import flask_whooshalchemy as whooshalchemy

secret_key = os.environ['APP_SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

class User(db.Model):
	__table_args__ = {'extend_existing': True}
	__searchable__ = ['username']

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
	biography = db.Column(db.String(200))
	verified = db.Column(db.Boolean)
	photo = db.Column(db.String(150))


	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)


	def __init__(self, id, email, username, password, forename, surname, city, biography, confirmationToken, passwordToken, verified, photo):
		self.id = id
		self.email=email
		self.username=username
		self.password=password
		self.forename=forename
		self.surname=surname
		self.city=city
		self.biography=biography
		self.confirmationToken=confirmationToken
		self.passwordToken=passwordToken
		self.verified=verified
		self.photo=photo


	def __repr__(self):
		return '<Username %r>' % self.username



class Post(db.Model):
	__table_args__ = {'extend_existing': True}
	__searchable__ = ['author', 'postedOn', 'city', 'postContent']

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	author = Column(Integer, ForeignKey('user.id'))
	postedOn = db.Column(db.String(60))
	postContent = db.Column(db.String(60))
	likesCount = db.Column(db.String(5), default=0)
	image = db.Column(db.String(250))
	city = db.Column(db.String(15))
	coordinates = db.Column(db.String)
	appreaciated = db.Column(db.Boolean)
	isPanorama = db.Column(db.Boolean)
	#a user can have many posts, so the relationship is many to one, from post to user
	user = db.relationship("User")
	comments = db.relationship('Comment')
	likes = db.relationship("Like")


	def __init__(self, id, author, postedOn, postContent, likes, image, city, coordinates, appreaciated, isPanorama):
		self.id = id
		self.author=author
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


# a leader has followers
# a follower has a leader

class Followers(db.Model):
	__table_args__ = {'extend_existing': True}

	id=db.Column(db.Integer, primary_key=True, nullable=False)
	#maxLength is 6 digits, so one per column
	leader = db.Column(db.Integer, nullable=False, primary_key=False)
	#follower is ForeignKey because we want the followers details, not the leaders, we already have those.
	follower = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)


	user = db.relationship("User")

	def __init__(self, id, leader, follower):
		self.id=id
		self.leader=leader
		self.follower=follower

	def __repr__(self):
		return '<leader %r>' % self.leader


class Like(db.Model):
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	postID = db.Column(db.Integer, ForeignKey('post.id'), nullable=False, primary_key=False)
	userID = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)

	user = db.relationship("User")
	post = db.relationship("Post")

	def __init__(self, id, postID, userID):
		self.id=id
		self.postID=postID
		self.userID=userID

	def __repr__(self):
		return '<Liked By %r>' % self.UserID


class Comment(db.Model):
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	postID = db.Column(db.Integer, ForeignKey('post.id'), nullable=False, primary_key=False)
	userID = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
	comment = db.Column(db.String(60), nullable=False)

	user = db.relationship("User")
	post = db.relationship("Post")

	def __init__(self, id, postID, userID, comment):
		self.id=id
		self.postID=postID
		self.userID=userID
		self.comment=comment

	def __repr__(self):
		return '<Comment %r>' % self.comment

#whooshalchemy.whoosh_index(app, Post)
#whooshalchemy.whoosh_index(app, User)
