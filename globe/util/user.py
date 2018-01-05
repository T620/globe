#used to handle user authentication, registration, and user's folder
from globe import models, app, Bcrypt
from globe.models import User
import uuid
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

def get_id(username):

	user = User.query.filter_by(username=unicode.title(username)).first()
	print user.id
 	return user.id


def exists(userid):

	checkUser = User.query.filter_by(id=userid).count()

	if checkUser > 0:
		return True
	else:
		return False


def password_hash_matches(userid, password):

	storedPass = User.query.filter_by(id=userid).first()

	if storedPass.password == password:
		return True
	else:
		return False



def register(newUser):
	import string

	#generate some secure tokens
	from globe.util import id_gen

	userID = id_gen.user_id(5, string.digits)

	username = id_gen.username(newUser['forename'], newUser['surname'])

	passwordToken = uuid.uuid4().hex
	confirmToken = uuid.uuid4().hex

	#for the time being, the users city wont be verified

	#add the user to User
	newAccount = User(
		id=userID,
		email=newUser['email'],
		username=username,
		forename=unicode.title(newUser['forename']),
		surname=unicode.title(newUser['surname']),
		password=newUser['password'],
		confirmationToken=confirmToken,
		passwordToken=passwordToken,
		city=newUser['city'],
		followers=0,
		following="None",
		biography="None",
		verified="False"
	)


	try:
		db.session.add(newAccount)
		db.session.commit()

		return True
		print 'done'
		#return mkdirs(userID, None)

	except:
		print 'failed to add to db'
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



'''
def mkdirs(userID, postID):
	import os
	if postID is not None:
		#create a subfolder in user/posts/
		subfolder = userID + "profile/posts/" + postID
	else:
		#dont create a post subfolder
		subfolder = userID + "/profile/posts/"
		folder = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)


	os.mkdir(folder)

	return create_profile(userID, folder)
'''

'''def create_profile(userID, destFolder):
	#now the user has a folder, create their profile picture and cover photo
	import os
	import shutil

	subfolder="/profile_defaults/profile.png"

	src=os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
	print src

	src_files = os.listdir(src)

	try:

		for file_name in src_files:
    		full_file_name = os.path.join(src, file_name)
    		if (os.path.isfile(full_file_name)):
        		shutil.copy(full_file_name, destFolder)

		return True

	except:
		return False
'''
