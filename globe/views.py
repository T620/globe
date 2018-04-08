import os, uuid, random, string
from globe import app, db, mail
from flask import render_template, request, redirect, url_for, session, abort, g, jsonify, json
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
	from models import Post, User, Comment, Like
	#TO DO: filter and sort via POST
	posts = Post.query.all()
	comments = Comment.query.limit(2).all()
	likes = Like.query.all()

	return render_template("feed.html", posts=posts, key=os.environ['MAPS_API_KEY'], comments=comments, likes=likes)



@app.route("/post/new/", methods=["GET", "POST"])
@login_required
def upload():
	if request.method=="POST":
		from util import post

		formParams = {
			"file": request.files['image'],
			"user": session['g_user'],
			"desc": request.form['desc'],
			"city": request.form['location-city'],
			"coords": request.form['location-coords'],
			"pano": request.form['image-type']
		}
		if post.new(formParams):
			return redirect(url_for('load_feed'))
		else:
			return "oh shit"

@app.route("/post/<id>")
def load_post(id):
	if id == "new":
		return redirect(url_for('load_feed'))
	else:
		from models import Post, User

		#need the specific post
		post = Post.query.filter_by(id=id).first_or_404()

		#now we need the posters profile to show to the user
		#rofile = User.query.filter_by(username=post.author).first_or_404()
		backLink = request.referrer
		#render away
		#TODO: change this template to a card in feed,html to a link saying "view full profile"
		return render_template("lightbox.html", post=post, backLink=backLink)




'''
@app.route("/lookup/<place>", methods=["GET", "POST"])
def lookup(place):
	from util import places

	# check if the place entered was a county
	if places.determineCounty(place):
		# lookup the city of that county
		for county in json.parse(counties.json, 'r'):
			if place == county:
				return county

		filename = str(unicode.title(county)) + ".csv"
		with open(filename, 'rb') as csv:
			rows = csv.reader(csvfile, delimiter=' ', quotechar='|')
			for row in rows:
				print row
	else:
		return place
'''

#demoing the new db relationships
@app.route("/relationship/")
def demo():
	from models import Post, User

	me = User.query.filter_by(id=1587).first()
	print me.id

	postsByMe = Post.query.filter_by(author=me.id).first()

	return postsByMe.city

#problem: geocoding service in upload form sometimes returns district/county instead of city.
#need to add a method which fixes this in the future.
@app.route("/explore/", methods=["GET", "POST"])
def explore():
	location = request.args.get('filter', None)

	# if there is no filter in place
	if location is not None:
		location = unicode.title(location)
		#grab all the records from the database according to that location
		from models import Post

		posts = Post.query.filter_by(city=unicode.title(location)).all()
		postCount = Post.query.filter_by(city=unicode.title(location)).count()
		print "number of posts: %s" % postCount

		#check if that result yielded any results.
		if postCount < 1:
			#if the location provided by the user doesn't bring any results, ask the user to enter a place
			return render_template("explore.html", message="Your search didn't return any results. Try somewhere else.")
		else:
			center = posts[0].coordinates
			print 'defining center of map: %s' % center


			key = os.environ.get('MAPS_API_KEY')
			return render_template("map.html", posts=posts, key=key, count=postCount, center=center, location=location)

	else:
		#if the location provided by the user doesn't bring any results, ask the user to enter a place
		return render_template("explore.html")


@app.route("/search/", methods=["GET", "POST"])
def search():
	if request.method == "GET":
		return render_template("search.html")
	else:
		searchParams = request.form['params']
		category = request.form['category']

		if searchParams is not None and category is not None:
			# either Post or User
			# init users and posts to prevent ref before assignment erorr
			users = None
			posts = None
			if category == "user":
				from models import User

				users = User.query.whoosh_search(searchParams)
				count = User.query.whoosh_search(searchParams).count()
			else:
				from models import Post

				posts = Post.query.whoosh_search(searchParams)
				count = Post.query.whoosh_search(searchParams).count()

			return render_template("search_results.html", category=category, users=users, count=count, posts=posts)
		else:
			return "error. "


# Likes

@app.route("/add/like/", methods=["POST"])
def like_post():
	try:
		post = jsonify(request.json)
		data = json.loads(post.data)

	 	postID = str(data['id'])
		authorID = str(data['author'])
		str(postID)
		str(authorID)
	except Exception as e:
		print e
		abort(500)

	# look how long this logic statement is!
	if authorID is not None and postID is not None:
		from models import Like, Post
		likeID = Like.query.count()

		# check if the user's already liked this post
		like = Like.query.filter_by(postID=postID).filter_by(userID=authorID).first()
		count = Like.query.filter_by(postID=postID).filter_by(userID=authorID).count()
		if count > 0:
			print "already liked, unliking..."
			db.session.delete(like)
			db.session.commit()
			response = {"msg": "unliked"}
			return jsonify(response)
		else:
			new = Like(
				likeID + 1,
				postID,
				authorID,
			)
			likePost = Post.query.filter_by(id=postID).first()
			likePost.likesCount = (likePost.likesCount + 1)
			try:
				db.session.add(new)
				db.session.add(likePosts)
				db.session.commit()
				response = {"msg": "liked"}
				return jsonify(response)
			except Exception as e:
				print ("failed to save", e)
				return abort(500)
	else:
		print "author/post is none"
		return abort(500)


# Comments
@app.route("/add/comment/", methods=["POST"])
def add_comment():

	post = jsonify(request.json)
	data = json.loads(post.data)
	print data

 	post = str(data['id'])
	author = str(data['user'])
	comment = str(data['comment'])
	print post, author, comment

	# look how long this logic statement is!
	if comment is not None and author is not None and post is not None:
		from models import Comment
		commentID = Comment.query.count()

		# check if the user's commented on this post
		commentCheck = Comment.query.filter_by(postID=post).filter_by(userID=author).first()
		count = Comment.query.filter_by(postID=post).filter_by(userID=author).count()

		if count > 0:
			print "already commented, replacing comment..."
			commentCheck.comment = comment
			db.session.add(commentCheck)
			db.session.commit()
			response = {"msg": "updated"}
			return jsonify(response)

		new = Comment(
			commentID + 1,
			post,
			author,
			comment
		)
		try:
			db.session.add(new)
			db.session.commit()

			response = {"msg": "added"}
			return jsonify(response)
		except:
			print "fuck when adding to db"
			return abort(500)
	else:
		print abort(500)
# helpers for comments and links
@app.route("/test/")
def load():
	return "<!doctype html>"  + "<form action='/add/like/' method='post'><input type='text' name='author' value='96732' /> <input type='text' name='post' value='3' /><input type='submit' value='submit' />"

def get_comments(postID):
	from models import Comment

	comments = Comment.query.filter_by(id=postID).all()

	return comments

def count_comments(postID):
	from models import Comments
	count = Comment.query.filter_by(id=postID).count()
	return count

def get_likes(postID):
	from models import Like

	likes = Like.query.filter_by(id=postID).all()

	return likes

def count_likes(postID):
	from models import Like
	count = Like.query.filter_by(id=postID).count()
	return count

# only for usability, redirects to /profile/
@app.route("/user/")
@login_required
def redr_to_profile():
	return redirect(url_for('load_user', username=""))

# /user/<username> was old
@app.route("/profile/<username>")
def redir_to_load_user(username):
	return redirect(url_for('load_user', username=username))

@app.route("/user/profile/<username>")
def load_user(username):
	# loads another user's profile. This is not the user who is logged in.
	# if no username is specified, the route below will be triggered, which will load the logged in user
	if username is None:
		print 'username provided'
		return redirect(url_for('load_int_user'))
	else:
		return profile(username)


@app.route("/user/profile/")
@login_required
def load_int_user():
	# loads a user's profile based on their session
	if session['g_user'] is None:
		redirect(url_for('login'))
	else:
		user = session['g_user']
		from models import User
		user = User.query.filter_by(id=user).first()
		user = user.username
		return profile(user)

def profile(username):
	#shows a given profile or 404s if not found
	from models import User, Post, Followers
	master = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=master.id).all()

	#josh has followers:
	#  03114
	#  12335
	following = []
	#grab the followers
	#josh.followers = ['03114', '12335']
	followers = Followers.query.filter_by(leader=master.id).all()

	UserIsFollowing = Followers.query.filter_by(follower='1587').all()
	print UserIsFollowing

	for user in UserIsFollowing:
		print user.leader
		leader = User.query.filter_by(id=user.leader).first()

		print leader.forename
		following.append(leader)

	# now check the data was stored correctly
	for user in following:
		print user.forename

	if find(session['g_user']) == username:
		ownProfile = True
	else:
		ownProfile = False

	print "own profile: %s"  % ownProfile

	return render_template("user/profile.html", master=master, posts=posts, followers=followers, following=following, ownProfile=ownProfile)


#finds a users username based on userID
def find(id):
	from models import User
	person = User.query.filter_by(id=id).first()
	numRows = User.query.filter_by(id=id).count()
	if numRows > 0:
		return person.username
	else:
		return False



@app.route("/user/posts/")
def redr_to_all():
	#default is /all/, so redirect the user to prevent 404
	return redirect(url_for('load_users_posts', _filter='all'))


@login_manager.user_loader
def load_user(id):
	from models import User
	return User.query.get(unicode(id))



@app.route("/user/logout/")
def logout():
	logout_user()
	session['g_user'] = None
	print session['g_user']
	return redirect(url_for("load_index"))

@app.route('/user/login/', methods=["GET", "POST"])
def login():
	if request.method=="GET":
		return render_template("/user/login.html")
	else:
		from models import User

		email = request.form['email']
		password = request.form['password']

		#changed this from username to email
		userExists = User.query.filter_by(email=email).count()

		from util import _user
		if userExists > 0:
			user = User.query.filter_by(email=email).first()
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


@app.route('/user/register/', methods=["GET", "POST"])
def register():
	if request.method=="POST":
		print "posted"
		from models import User
		from util import _user

		newUser = {
			"forename": request.form['forename'],
			"surname": request.form['surname'],
			"email": request.form['email'],
			"password": request.form['password'],
			"city": "Edinburgh"
		}

		_user.register(newUser)

		#set_default_photos(username)

		return 'done'
		#mail.send_email(subject, sender, recipients, text_body, html_body)

			#return render_template('user/register_step-2.html', email=newUser['email'])
		#else:
			#return 'error when trying to add user to database :('
	else:
		return render_template("register.html")


@app.route("/user/register/auth/")
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


@app.route("/user/register/resend-email", methods=["GET", "POST"])
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



@app.route("/logout/")
def redr_to_logout():
	return redirect(url_for('logout'))

@app.route("/login/")
def redr_to_login():
	return redirect(url_for('login'))

@app.route("/register/")
def redr_to_register():
	return redirect(url_for('register'))


if __name__ == '__main__':
	app.run()
