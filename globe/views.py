import os, uuid, random, string
from globe import app, db, mail
from flask import render_template, request, redirect, url_for, session, abort, g
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt
import tinys3
from flask_cors import CORS, cross_origin
import geopy
from geopy.geocoders import Nominatim



CORS(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "login"


bcrypt = Bcrypt(app)

app.secret_key = os.environ['APP_SECRET_KEY']

UPLOAD_FOLDER = '/home/josh/projects/globe/globe/static/user_uploads/'

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
def load_index():
	#both conditions return true if the user is logged in
	if current_user.is_active and current_user.is_authenticated:
			print "Current User: %s" % current_user.username
			return redirect(url_for('load_feed'))
	else:
		return render_template("index.html")


@app.route("/feed/")
def load_feed():
	from models import Post

	posts = Post.query.all()

	key = os.environ.get('MAPS_API_KEY')

	return render_template("feed.html", posts=posts, key=key)


@app.route("/test")
def test():
	#used to translate an address to a set of coordinates
	from util import coordinates

	latAndLong = coordinates.get("Edinburgh")

	return latAndLong



@app.route("/post/", methods=["GET", "POST"])
@login_required
def upload():
	if request.method=="POST":
		file = request.files['image']
		file.filename = "globe_pub_image"

		#generate a file name
		print session['g_user']
		from util import id_gen
		filename = str(session['g_user']) + "/" + id_gen.booking_id() + "_" + file.filename
		dest = app.config['UPLOAD_FOLDER'] + filename
		print dest

		try:
			from util import image
			image.crop(file, dest)
		except:
			return "could not save file: %s" % dest


		f = open(dest, 'rb')
		conn = tinys3.Connection(os.environ['S3_PUB_KEY'], os.environ['S3_PRIVATE_KEY'], tls=True)

		#filename variable matches the url structure of S3 exactly, so I can reuse it here
		url = 'static/user_uploads/' + filename

		try:
			print 'uploaded!'
			conn.upload(url, f, os.environ['S3_BUCKET_NAME'])
		except:
			return "error uploading"


		#example: s3.amazonaws.com/bucket/static/user_uploads/user/1235225412e21.jpg
		postUrl = os.environ['S3_ENDPOINT'] + "/" + os.environ['S3_BUCKET_NAME'] + "/" + url


		from util import geocoder
		#get the name of the city
		city = request.form['location-city']

		#this is already handled by gmaps
		#latAndLong = geocoder.getCoordinates(location)
		#grab coordinates of map pin

		coords = request.form['location-coords']
		imageType = request.form['image-type']

		print "image is panorama: %s " % imageType

		from util import clock
		timeStamp = str(clock.timeNow())

		#add post to Posts
		from models import Post
		postCount = Post.query.count()
		postCount = postCount + 1

		print session['g_user']
		print postCount
		print timeStamp
		post = Post (
			postCount,
			session['g_user'],
			timeStamp,
			request.form['desc'],
			"0",
			postUrl,
			city,
			coords,
			True,
			imageType
		)

		db.session.add(post)
		db.session.commit()

		return redirect(url_for('load_feed'))

	else:
		return redirect(url_for('load_feed'))


#problem: geocoding service in upload form sometimes returns district/county instead of city.
#need to add a method which fixes this in the future.
@app.route("/explore/", methods=["GET", "POST"])
def explore():
	location = request.args.get('filter', None)

	# if there is no filter in place
	if location is not None:
		#grab all the records from the database according to that location
		from models import Post

		posts = Post.query.filter_by(city=unicode.title(location)).all()
		postCount = Post.query.filter_by(city=unicode.title(location)).count()
		print "number of posts: %s" % postCount

		#check if that result yielded any results.
		if postCount < 1:
			#if the location provided by the user doesn't bring any results, ask the user to enter a place
			return render_template("map_get_location.html")
		else:
			center = posts[0].coordinates
			print 'defining center of map: %s' % center


			key = os.environ.get('MAPS_API_KEY')
			return render_template("map.html", posts=posts, key=key, count=postCount, center=center, location=location)

	else:
		#if the location provided by the user doesn't bring any results, ask the user to enter a place
		return render_template("map_get_location.html")


'''def teleporter():
	from models import Post
	print 'not got a country via GET or POST. finding random, brb...'
	#user used GET with no search parameters (no location provided)

	randomPost = Post.query.order_by(Post.id.desc()).first()

	#return the function with a new location, which is the last one which was entered into the database
	print '***Found! Result: %s'  % randomPost.city

	#	resultMsg = "We couldn't find the place you asked for, so here is a random location instead."

	#im having to create a session because explore asks for zero parameters, so when we pass one here it throws an error.
	#hardcoded to edinburgh atm
	session['random_location'] = "Edinburgh"
	return explore()
'''

@app.route("/user/")
@login_required
def redr_to_profile():
	return redirect(url_for('load_int_user'))


#this is the current user's personal profile
@login_required
@app.route("/user/profile/")
def load_int_user():
	#grab the users details
	from models import User
	user = User.query.filter_by(id=session['g_user']).first_or_404()

	if user is not None:
		return render_template("user/profile.html", user=user)
	else:
		return "User not found after logging in??"


#external user (not the person logged in, someone else)
@app.route("/user/<username>")
def load_ext_user(username):
	#grab the user's basic profile info
	from models import User, Post
	user = User.query.filter_by(username=unicode.title(username)).first_or_404()

	return render_template("user/profile.html", user=user)



@app.route("/user/posts/")
def redr_to_all():
	#default is /all/, so redirect the user to prevent 404
	return redirect(url_for('load_users_posts', _filter='all'))


@login_manager.user_loader
def load_user(id):
	from models import User
	return User.query.get(unicode(id))


@app.route('/login/', methods=["GET", "POST"])
def login():
	if request.method=="GET":
		return render_template("/user/login.html")
	else:
		from models import User

		username = request.form['username']
		password = request.form['password']

		#changed this from username to email
		userExists = User.query.filter_by(email=unicode.title(username)).count()

		from util import _user
		if userExists > 0:
			user = User.query.filter_by(username=unicode.title(username)).first()
			print "[info] user id: %s " % user.id
			if _user.password_hash_matches(user.id, password):
				login_user(user)
				session['g_user'] = user.id
				print session['g_user']
				return redirect(request.args.get("next") or url_for("load_index"))
			else:
				return "password invalid :("
		else:
			return "User does not exist."


@app.route('/register/', methods=["GET", "POST"])
def register():
	if request.method=="POST":
		print "posted"
		from util import _user

		newUser = {
			"forename": request.form['forename'],
			"surname": request.form['surname'],
			"email": request.form['email'],
			"password": request.form['password'],
			"city": "Edinburgh"
		}


		if _user.register(newUser):
																									#TODO: user now needs to login via email
			return render_template('user/register_step-2.html', username=newUser['email'])
		else:
			return 'error when trying to add user to database :('
	else:
		return render_template("register.html")



@app.route("/register/auth/")
def confirm_new_user():
	#user didnt post anything, so they've accessed this URL from their email
	token = request.args.get("token", None)
	username = request.args.get("username", None)

	if token is not None and username is not None:
		#no need to check CSRF here
		from models import UserAuth
		from util import user, email

		if util.authorise(token, username):
			#send the user a confirmation email
			from mail import send_email
			subject = "Globe: New Account"
			sender=["no-reply@globe.com"]
			recipients=user.email.split(" ")
			text_body="Welcome!"
			html_body=render_template("user/new_account.html", username=username)

			return render_template('user/register_step-3.html')
		else:
			return "error"

	else:
		return "invalid token/username combination"




@app.route("/register/resend-email", methods=["GET", "POST"])
def resend_email():
	if request.method == "POST":
		username = request.args.get("username", None)
		if username is not None:
			#create a new confirm token and send them it.
			from models import UserAuth
			user = UserAuth.query.filter_by(username=username).first_or_404()

			confirmToken = uuid.uuid4().hex
			user.confirmationToken = confirmToken

			db.session.add(user)
			db.session.commit()

			#resend the email
			emailTo = user.email.split(" ")

			#send the user a confirmation email
			from mail import send_email
			subject = "Globe: New Account"
			sender=["no-reply@globe.com"]
			recipients=emailTo
			text_body="Welcome!"
			html_body=render_template("user/new_account.html", username=username)

			return "email re-sent!"

	else:
		abort(403)




if __name__ == '__app__':
	app.debug=True
	app.run(host='0.0.0.0', port=5000)
