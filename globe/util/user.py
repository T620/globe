#used to handle user authentication, registration, and user's folder

def get_id(username):
	from models import User

	user = User.query.filter_by(username=username).first()

 	return user.id


def exists(userid):
	from models import User

	checkUser = UserAuth.query.filter_by(id=userid).first.count()

	if checkUser > 0:
		return True
	else:
		return False

def password_hash_matches(userid, password):
	from models import UserAuth

	hashedPassword = UserAuth.query.filter_by(id=userid).first()

	if bcrypt.check_password_hash(hashedPassword, password):
		return True
	else:
		return False



def register(newUser):
	from models import User, UserAuth
	import string

	#hash their password
	hashedPassword = bcrypt.generate_password_hash(password).decode("UTF-8")

	#generate some secure tokens
	from globe.util import id_gen, clock

	userID = id_gen.user_id(5, string.digits)

	username = id_gen.username(newUser['forename'], newUser['surname'])

	passwordToken = uuid.uuid4().hex
	confirmToken = uuid.uuid4().hex

	fullname = unicode.title(newUser['forename']) + unicode.title(newUser['surname'])

	todaysDate = clock.timeNow()

	#for the time being, the users city wont be verified

	#add the user to UserAuth
	newAccount = User(
		id=userID,
		email=newUser['email'],
		username=username,
		fullname=fullName,
		city=newUser['city'],
		followers=0,
		following="None"
		biography="None"
	)

	newAccountAuth = UserAuth(
		id=userID,
		email=newUser['email'],
		username=username,
		password=hashedPassword,
		registeredOn=todaysDate,
		lastLogin="None",
		lastIPUsed=snooper.getUserIP(),
		verified="False"
	)

	try:
		db.session.add(newAccount)
		db.session.add(newAccountAuth)
		db.session.commit()

		return mkdirs(userID, None)

	except:
		return False


def authorise(token, username):
	from models import UserAuth

	user = UserAuth.query.filter_by(username=username).first_or_404()
	if token == user.confirmationToken:
		#verify the new account
		print "[INFO]: tokens match. Tokens: %s" % token + ", " + user.confirmationToken

		user.verified=True

		db.session.add(user)
		db.session.commit()

		return True
	else:
		return False




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


def create_profile(userID, destFolder):
	#now the user has a folder, create their profile picture and cover photo
	import os
	import shutil

	subfolder="/profile_defaults/profile.png"

	src=os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
	print src

	src_files = os.listdir(src)

	try:

		for file_name in src_files:
    		full_file_name = os.path.join(src, 	file_name)
    		if (os.path.isfile(full_file_name)):
        		shutil.copy(full_file_name, destFolder)

		return True

	except:
		return False
