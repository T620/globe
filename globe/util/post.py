from werkzeug.utils import secure_filename
import os, string
from globe import app, db
from globe import models
from globe.models import Post
from flask import session
from globe.util import id_gen, clock


def new(formParams):
	file = formParams['file']
	filename = file.filename
	print formParams['pano']

	if check(file, filename):
		save_locally(file, filename, formParams)
	else:
		return False
def check(file, filename):
		#test the file for filename and width
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			return True

		else:
			return False


allowedExtensions= set(['jpg', 'jpeg', 'png'])
def allowed_file(filename):
	return '.' in filename and \
	filename.rsplit('.', 1)[1].lower() in allowedExtensions

def save_locally(file, filename, formParams):
		print 'saving'

		postID = id_gen.postID(4, string.digits, session['g_user'])
		dest = os.environ['UPLOAD_PATH']  + str(session['g_user']) + "/posts/" + str(postID) + "/"

		os.mkdir(dest)
		filePath = os.path.join(dest + filename)
		file.save(filePath)

		if formParams['pano'] == "True":
			filePath = os.path.join(dest + filename)
			crop(filePath, filename)

		return create(filePath, formParams)

def create(dest, formParams):
		#adds post to database
		postCount = Post.query.count()
		postCount = postCount + 1

		post = Post(
			id=postCount,
			author=formParams['user'],
			postedOn=str(clock.timeNow()),
			postContent=formParams['desc'],
			likes="0",
			image=dest,
			city=formParams['city'],
			coordinates=formParams['coords'],
			appreaciated=True,
			isPanorama=formParams['pano']
		)
		db.session.add(post)
		db.session.commit()

		return True

# Helpers
def crop(file, filename):
		print file
		from wand.image import Image

		with open(file) as f:
			image_binary = f.read()


		with Image(blob=image_binary) as img:
			width = img.width
			height = img.height

			#if the width of an image is wider than 4096px, crop the width, but leave the height
			if width > 4096:
				print "Image too wide, cropping width"
				img.crop(0, 0, 4096, height)
				img.save(filename=filename)

			else:
				print "image is less than 4096px wide, saving"
				img.save(filename=filename)




'''  DEPRECATED
def upload(modifiedFile, formParams):
		filename = modifiedFile.filename
		postID = id_gen.postID(4, string.digits, session['g_user'])

		dest = str(session['g_user']) + "/posts/" + str(postID) + "/"
		# uploads the file to S3
		print modifiedFile
		print "dir: %s" % dest


		s3 = boto3.client(
	   		"s3",
	   		aws_access_key_id=os.environ['S3_PUB_KEY'],
	   		aws_secret_access_key=os.environ['S3_PRIVATE_KEY']
		)
		try:
			s3.upload_fileobj(
				modifiedFile,
				os.environ['S3_BUCKET_NAME'],
				#TO DO: modify this param to use the correct path, as the above only takes the bucket name, need to add /static/user_... etc
				dest + filename,
				ExtraArgs={
					"ACL": "public-read",
					"ContentType": modifiedFile.content_type
				}
			)
		except Exception as e:
			# This is a catch all exception, edit this part to fit your needs.
			print("Something Happened: ", e)
			return False

		url = os.environ['S3_ENDPOINT'] + "/" + os.environ['S3_BUCKET_NAME'] + "{}{}".format(dest, filename)

		return create(url, formParams)
'''


'''
dest = app.config['UPLOAD_FOLDER'] + str(session['g_user']) + "/posts/" + str(postID) + "/"
print dest

#if the image is a panorama, check the width
# if it needs to be cropped, save it then update the folder
if request.form['image-type'] == "True":
	print "creating temp directory to crop"
	tempDir = os.environ['TEMP_FILE_CACHE'] + file.filename
	file.save(tempDir)
	crop(tempDir)
	dest = tempDir

	#use the cropped image
	with open(tempDir) as f:
		file = f

if files.passes_checks(file, dest, isPanorama):
	if files.upload_to_s3(file, dest):

		return redirect(url_for('load_feed'))

	else:
		return "File failed to upload!"

else:
	return "File failed checks!"

else:
return redirect(url_for('load_feed'))
'''
