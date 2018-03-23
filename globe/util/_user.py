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


def set_default_photos(url):
	import os, tinys3, string
	from globe import app

	#init conection to S3
	conn = tinys3.Connection(os.environ['S3_PUB_KEY'], os.environ['S3_PRIVATE_KEY'], tls=True)

	# create the user's s3 subdir + image path
	#josh.tait912/profile/placeholder.jpg

	photo = app.config['UPLOAD_FOLDER'] + "profiles/placeholder.jpg"
	
	if os.environ['FILE_STORAGE_LOC'] == "LOCAL":
		print 'saving file locally'
	else:
		print 'saving file to S3'
		#now the file and path are ready, save the file to the user's folder in s3
		f = open(photo, 'rb')
		conn.upload(url, f, os.environ['S3_BUCKET_NAME'])
		#https://s3.aws.com/endpoint/bucket/static/user_uploads/josh.tait516/profile/placeholder.jpg
		#photoUrl = os.environ['S3_ENDPOINT'] + "/" os.environ['S3_BUCKET_NAME'] + url

		print "uploaded default profile photo, creating user_uploads subdir..."

def register(newUser):
	from globe import app, db
	import os, tinys3, string
	from globe.util import id_gen, mail


	userID = id_gen.user_id(5, string.digits)
	username = id_gen.username(newUser['forename'], newUser['surname'])
	passwordToken = uuid.uuid4().hex
	confirmToken = uuid.uuid4().hex

	url = app.config['UPLOAD_FOLDER'] + str(userID) + "/profile/" + 'placeholder.jpg'
	#url = '/static/user_uploads/' + str(userID) + "/profile/" + 'placeholder.jpg'

	#photoUrl = "https://s3.us-west-2.amazonaws.com/elasticbeanstalk-us-west-2-908893185885" + url

	print url
	set_default_photos(url)

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
		photo=url
	)

	db.session.add(newAccount)
	db.session.commit()

	print 'user added, creating post subdirectory'

	import os
	subfolder = userID + "/profile/posts/"
	folder = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
	os.makedirs(folder)

	print 'subdirectory added'




def create_post_folder(userID, postID):
	import os
	subfolder = userID + "/profile/posts/" + postID

	folder = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)

	try:
		os.mkdir(folder)
		return True
	except:
		return False


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
