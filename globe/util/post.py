from werkzeug.utils import secure_filename
import os, string
from globe import app, db
from globe import models
from globe.models import Post
from flask import session
from globe.util import id_gen, clock
import boto3

def new(formParams):
	file = formParams['file']
	filename = file.filename
	print formParams['pano']

	if check(file, filename, formParams):
		if upload_to_s3(file, filename, formParams):
			return True
	else:
		return False

def check(file, filename, formParams):
		#test the file for filename and width
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			if formParams['pano'] == "True":
				crop_if_too_wide(file, filename, formParams)
				#image is uploaded from the crop_if_too_wide function here
			else:
				print "image is 2d, not checking width"
				cache = os.environ['LOCAL_STORAGE_CACHE']
				# need to add filename to save it
				filename = "altered_" + filename
				destAndName = cache + "/" + filename
				file.save(destAndName)

				upload_to_s3(destAndName, filename, formParams)

		else:
			return False

'''def save_locally(file, filename, formParams):
		print 'saving'

		postID = id_gen.postID(4, string.digits, session['g_user'])
		dest = os.environ['UPLOAD_PATH']  + str(session['g_user']) + "/posts/" + str(postID) + "/"

		os.mkdir(dest)
		filePath = os.path.join(dest + filename)
		file.save(filePath)

		if formParams['pano'] == "True":
			filePath = os.path.join(dest + filename)
			crop(filePath, filename)

		return create(filePath, formParams) '''

def upload_to_s3(filePath, filename, formParams):
	#uploads the image to S3 after cropping etc
	postID = id_gen.postID(4, string.digits, session['g_user'])
	dest = str(session['g_user']) + "/posts/" + str(postID) + "/"
	print dest
	print filename
	print filePath
	with open(filePath, 'rb') as image:

		print "image now: %s" % image

		s3 = boto3.client(
			"s3",
			aws_access_key_id=os.environ['S3_PUB_KEY'],
			aws_secret_access_key=os.environ['S3_PRIVATE_KEY']
		)
		try:
			print "trying to upload..."
			s3.upload_fileobj(
				image,
				os.environ['S3_BUCKET_NAME'],
				#TO DO: modify this param to use the correct path, as the above only takes the bucket name, need to add /static/user_... etc
				dest + filename,
				ExtraArgs={
					"ACL": "public-read"
				}
			)
			print "done!"
			url =  "https://" + os.environ['S3_ENDPOINT'] + "/" + os.environ['S3_BUCKET_NAME'] + "/" + dest + filename
			print url
			#delete the modified file from the system
			os.remove(filePath)
			return create(url, formParams)

		except Exception as e:
			# This is a catch all exception, edit this part to fit your needs.
			print("Something Happened: ", e)
			return False

		image.close()



def create(url, formParams):
		print "creating new post..."
		#adds post to database
		postCount = Post.query.count()
		postCount = postCount + 1

		post = Post(
			id=postCount,
			author=formParams['user'],
			postedOn=str(clock.timeNow()),
			postContent=formParams['desc'],
			likes="0",
			image=url,
			city=formParams['city'],
			coordinates=formParams['coords'],
			appreaciated=True,
			isPanorama=formParams['pano']
		)
		db.session.add(post)
		db.session.commit()
		print "did-diddly-done!"

		return True



# Helpers
def crop_if_too_wide(file, filename, formParams):
		cache = os.environ['LOCAL_STORAGE_CACHE']

		# need to add filename to save it
		destAndName = cache + filename

		try:
			file.save(destAndName)
			print ("saved to: ", destAndName)
		except Exception as error:
			print ("couldn't save file: " , error)
			return file

		from wand.image import Image
		from wand.display import display

		img = Image(filename=destAndName)
		print img
		width = img.width
		height = img.height

		with img.clone() as i:
			#if the width of an image is wider than 4096px, crop the width, but leave the height
			if width > 4096:
				print "Image too wide, cropping width"
				i.crop(0, 0, 4096, height)

				# file doesn't overwrite, so give it a new name
				name = cache +  "-" + filename
				print name
				i.save(filename=name)
				#delete old file
				os.remove(destAndName)

			else:
				print "image is less than 4096px wide, skipping"


		return upload_to_s3(name, filename, formParams)



allowedExtensions= set(['jpg', 'jpeg', 'png'])
def allowed_file(filename):
	return '.' in filename and \
	filename.rsplit('.', 1)[1].lower() in allowedExtensions


'''def upload(modifiedFile, formParams):
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
