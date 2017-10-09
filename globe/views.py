import os, uuid, random, string
from globe import app, db, mail
from flask import render_template, request, redirect, url_for, session, abort
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "login"


bcrypt = Bcrypt(app)

@app.route('/')
def load_index():
	return render_template("index.html")


@app.route('/login/')
def login():
	return 'yeah'

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


		#build the query
		newAccount = User(
			#just call it here
			id = userID,
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

		auth = UserAuth(
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
		html_body=render_template("confirm_email.html", username=auth.username, token=confirmToken)
		send_email(subject, sender, recipients, text_body, html_body)

		db.session.add(newAccount)
		db.session.add(auth)
		db.session.commit()

		return "You've successfully created your account. Please wait while your account is confirmed. You will be contacted via email when this is done."

	else:
		return render_template("register.html")





if __name__ == '__app__':
	app.debug=True
	app.run(host='0.0.0.0', port=5000)
