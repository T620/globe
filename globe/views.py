import os, uuid, random, string
from globe import app, db, mail
from flask import render_template, request, redirect, url_for, session, abort
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
import tinys3

CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "login"


bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(userid):
	from models import UserAuth
	user = UserAuth.query.filter(UserAuth.id==userid).first()
	session['user'] = user.id
	print "[INFO]: Current User: %s" % session['user']
	print "aka %s" % user.username
	return user

@app.route('/')
def load_index():
	return render_template("index.html")

@app.route("/feed/")
@cross_origin()
def load_feed():
	return render_template("feed.html")



@app.route("/upload/", methods=["GET", "POST"])
def upload():
		conn = tinys3.Connection(os.environ['S3_PUB_KEY'], os.environ['S3_PRIVATE_KEY'], tls=True)
		print conn

		f = open('/home/josh/projects/globe/globe/static/img/test.jpg','rb')

		url = 'static/user_uploads/jt3/file.jpg'

		try:
			conn.upload(url, f, os.environ['S3_BUCKET_NAME'])
			return 'file uploaded!'
		except:
			return "error when trying to upload file!"




@app.route("/explore/")
def explore():
	return 'enter a country'


@app.route("/map/")
def load_map():
	from models import Post
	products = Post.query.filter_by(status="Available").all()
	count = Post.query.filter_by(status="Available").count()

	#Grab the API key for GMaps
	key = os.environ.get('MAPS_API_KEY')

	return render_template("map.html", products=products, key=key, count=count)


@app.route("/user/")
def redr_to_profile():
	return redirect(url_for('load_int_user'))


#this is the current user's personal profile
@login_required
@app.route("/user/profile/")
def load_int_user():
	#grab the users details
	from models import User
	user = User.query.filter_by(id=session['user']).first_or_404()

	if user is not None:
		return render_template("user/profile.html", user=user)
	else:
		return "User not found after logging in??"


#external user (not the person logged in, someone else)
@app.route("/user/<username>")
def load_ext_user(username):
	#grab the user's basic profile info
	from models import User, Post, Booking
	user = User.query.filter_by(username=unicode.title(username)).first_or_404()

	return render_template("user/ext_profile.html", user=user, itemsBorrowed=None)



@app.route("/user/posts/")
def redr_to_all():
	#default is /all/, so redirect the user to prevent 404
	return redirect(url_for('load_users_posts', _filter='all'))


@app.route('/login/', methods=["GET", "POST"])
def login():
	if request.method=="GET":
		return render_template("/user/login.html")
	else:
		username = request.form['username']
		password = request.form['password']

		from util import user
		userID = user.get_id(username)

		if user.exists(userID):
			if password_hash_matches(userID, password):
				login_user(user)
			else:
				return "password invalid :("
		else:
			return "User does not exist."


@app.route('/register/', methods=["GET", "POST"])
def register():
	if request.method=="POST":
		from util import user

		newUser = {
			"forename": request.form['forename'],
			"surname": request.form['surname'],
			"email": request.form['email'],
			"password": request.form['password'],
			"city": request.form['city']
		}

		if user.register(newUser):
			return render_template('user/register_step-2.html', username=newAccountAuth.username)
		else:
			return "error."
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
