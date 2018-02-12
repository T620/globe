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
	import os
	import tinys3
	import string
	from globe import db
	print db

	print newUser['forename']
	#generate some secure tokens
	from globe.util import id_gen

	userID = id_gen.user_id(5, string.digits)

	username = id_gen.username(newUser['forename'], newUser['surname'])

	passwordToken = uuid.uuid4().hex
	confirmToken = uuid.uuid4().hex

	#for the time being, the users city wont be verified

	#init conection to S3
	conn = tinys3.Connection(os.environ['S3_PUB_KEY'], os.environ['S3_PRIVATE_KEY'], tls=True)


	#give the file a name
	#josh.tait912/profile/placeholder.jpg
	filename = str(username) + "/" + "profile/" + 'placeholder.jpg'
	#filename variable matches the url structure of S3 exactly, so I can reuse it here
	url = 'static/user_uploads/' + filename

	#now the file and path are ready, save the file to the user's folder in s3
	photo = app.config['UPLOAD_FOLDER'] + "profiles/placeholder.jpg"
	f = open(photo, 'rb')

	try:
		print 'uploaded!'
		conn.upload(url, f, os.environ['S3_BUCKET_NAME'])
	except:
		return "error uploading"

	#https://s3.aws.com/endpoint/bucket/static/user_uploads/josh.tait516/profile/placeholder.jpg
	#photoUrl = os.environ['S3_ENDPOINT'] + "/" os.environ['S3_BUCKET_NAME'] + url
	photoUrl = "https://s3.us-west-2.amazonaws.com/elasticbeanstalk-us-west-2-908893185885/" + url
	print photoUrl

	#add the user to User
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
		followers=0,
		following="None",
		biography="None",
		verified="False",
		photo=photoUrl
	)

	db.session.add(newAccount)
	db.session.commit()


	'''try:


		return True
		print 'done'
		#return mkdirs(userID, None)

	except:
		print 'failed to add to db'
		return False
		'''
	return True


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
