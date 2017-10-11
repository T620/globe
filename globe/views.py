import os, uuid, random, string
from globe import app, db, mail
from flask import render_template, request, redirect, url_for, session, abort
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "login"


@login_manager.user_loader
def load_user(userid):
	from models import UserAuth
	return UserAuth.query.filter(UserAuth.id==userid).first()

bcrypt = Bcrypt(app)

@app.route('/')
def load_index():
	return render_template("index.html")

@app.route("/feed/")
@login_required
def load_feed():
	return render_template("feed.html")

@app.route('/login/', methods=["GET", "POST"])
def login():
	if request.method=="GET":
		return render_template("/user/login.html")
	else:
		from models import UserAuth
		user = UserAuth.query.filter_by(username=request.form['username']).first()
		if user is not None:
			print "[INFO]: User exists, checking password"
			#check if the user is verified
			if user.verified == True:
				if bcrypt.check_password_hash(user.password, request.form['password']):
					print "[INFO]: Password hash matches. Logging in..."
					login_user(user)
					#return redirect(url_for('admin_area'))
					return redirect(request.args.get('next') or url_for('load_feed') )
				else:
					print "[INFO]: User password hash failed to match!"
					return "incorrect password :("
			else:
				return "You can't log in until you confirm your account. Please check your email inbox"
		else:
			return "User does not exist."


@app.route('/register/', methods=["GET", "POST"])
def register():
	if request.method=="POST":
		from models import User
		#create unique details like username and tokens
		userID = User.query.count()
		userID +=1

		print "[INFO]: New User. ID: %s " % userID

		password=request.form['password']

		#hash the password and generate a reset token in case the user forgets their password
		hashedPassword = bcrypt.generate_password_hash(password).decode("UTF-8")
		resetToken = uuid.uuid4().hex
		confirmToken = uuid.uuid4().hex

		print "[INFO]: Hash = %s" % hashedPassword
		print "[INFO]: Reset Key = %s" % resetToken
		print "[INFO]: Confirm Token = %s" % confirmToken

		email = request.form['email']


		#add basic profile details to User
		newAccount = User(
			id=userID,
			email=email,
			username=request.form['forename'] + '.' + request.form['surname'] + "56",
			forename=request.form['forename'],
			surname=request.form['surname'],
			city=" ",
			followers=0,
			following="None",
			biography="Tell us about yourself"
		)

		#now add the secure details to UserAuth
		from models import UserAuth
		newAccountAuth = UserAuth(
			id=userID,
			email=email,
			username=request.form['forename'] + '.' + request.form['surname'] + "56",
			password=hashedPassword,
			registeredOn = "09-10-17:17:05:00",
			confirmationToken=confirmToken,
			passwordToken=resetToken,
			lastLogin="None",
			lastIPUsed="192.168.1.7",
			verified=False
		)


		emailTo = email.split(" ")
		from mail import send_email
		subject = "Globe: Confirm your account"
		sender = "no-reply@globe.com"
		recipients = emailTo
		text_body="Hi!"
		html_body=render_template("user/confirm_email.html", username=newAccountAuth.username, token=confirmToken)
		send_email(subject, sender, recipients, text_body, html_body)

		#commit the data
		db.session.add(newAccount)
		db.session.add(newAccountAuth)
		db.session.commit()

		return render_template('user/register_step-2.html', username=newAccountAuth.username)

	else:
		return render_template("register.html")



@app.route("/register/auth/")
def confirm_new_user():
	#user didnt post anything, so they've accessed this URL from their email
	token = request.args.get("token", None)
	username = request.args.get("username", None)
	print "[INFO] Token: %s" % token
	print "[INFO] Username: %s" % username

	if token is not None and username is not None:
		#no need to check CSRF here
		from models import UserAuth
		#if the token matches the token in the url, it's the correct user
		user = UserAuth.query.filter_by(username=username).first_or_404()
		if token == user.confirmationToken:
			#verify the new account
			print "[INFO]: tokens match. Tokens: %s" % token + ", " + user.confirmationToken

			user.verified=True

			db.session.add(user)
			db.session.commit()

			print 'new user confirmed'

			#now send the user their username and tell them that their account is verified/confirmed
			#send_email() doesnt accept a string format, so convert the variable into a list with a single item
			emailTo = user.email.split(" ")

			#send the user a confirmation email
			from mail import send_email
			subject = "Globe: New Account"
			sender=["no-reply@globe.com"]
			recipients=emailTo
			text_body="Welcome!"
			html_body=render_template("user/new_account.html", username=username)

			return render_template('user/register_step-3.html')

		else:
			return "tokens do not match"

	else:
		return 'tokens are invalid'



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
