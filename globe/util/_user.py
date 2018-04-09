#used to handle user authentication, registration, and user's folder
from globe import app
from globe.models import User

import uuid

def get_id(username):
	user = User.query.filter_by(username=unicode.title(username)).first()
 	return user.id



def password_hash_matches(userid, password):

	storedPass = User.query.filter_by(id=userid).first()

	if storedPass.password == password:
		return True
	else:
		return False


def register(newUser):
	from globe import app, db
	import os, tinys3, string
	from globe.util import id_gen, mail


	userID = id_gen.user_id(5, string.digits)
	username = id_gen.username(newUser['forename'], newUser['surname'])
	passwordToken = uuid.uuid4().hex
	confirmToken = uuid.uuid4().hex

	url = "/static/user_uploads/profiles/placeholder/placeholder.jpg"
	#url = '/static/user_uploads/50123/profile/placeholder.jpg'

	stockImage = "http://" + os.environ['S3_ENDPOINT'] + "/" + os.environ['S3_BUCKET_NAME'] + url
	print stockImage

	newAccount = User(
		id=userID,
		email=newUser['email'],
		username=username,
		password=newUser['password'],
		confirmationToken=confirmToken,
		passwordToken=passwordToken,
		forename=unicode.title(newUser['forename']),
		surname=unicode.title(newUser['surname']),
		city=newUser['city'],
		biography="None",
		verified="False",
		photo=stockImage
	)

	db.session.add(newAccount)
	db.session.commit()

def authorise(token, username):

	user = User.query.filter_by(username=username).first_or_404()
	if token == user.confirmationToken:
		#verify the new account
		print "[INFO]: tokens match. Tokens: %s" % token + ", " + user.confirmationToken

		user.verified=True

		db.session.add(user)
		db.session.commit()

		return True
	else:
		return False
