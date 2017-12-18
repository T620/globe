#handles filtering of posts

def filter_by(primaryCriteria, secondaryCriteria):


#marks a post as appreaciated (featured for that location)
def appreciate(post):
	#a post is appreciated if it reaches over 200 likes for a particular location

	from globe.models import Post

	post = Post.query.filter_by(id=postID).first()

	if post.likes > 200:
		if post.appreciated == "True":
			print 'post is already appreciated, skipping'
		else:
			post.appreciated = "True"
			db.session.add(post)
			db.session.commit()
			return True
	else:
		return False


def add_like(postID, author):
	from globe.models import Post

	post = Post.query.filter_by(id=postID).first()

	if post.id is not None:
		post.likes =+ 1
		db.session.add(post)
		db.session.commit()
		return True
	else:
		return False
