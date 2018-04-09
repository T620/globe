#handles file uploads from the user
from werkzeug.utils import secure_filename
import os
from globe import app
from flask import session

allowedExtensions= set(['jpg', 'jpeg', 'png'])

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in allowedExtensions


def passes_checks(file, dest):
	#returns True if the file is allowed, and if it's a pano, crop it accordingly
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		print 'file allowed...'
		print "dir: %s" % dest
		return True

	else:
		return False



def crop(dest):
	print file
	from wand.image import Image

	with open(dest) as f:
		image_binary = f.read()


	with Image(blob=image_binary) as img:
		width = img.width
		height = img.height

		#if the width of an image is wider than 4096px, crop the width, but leave the height
		if width > 4096:
			print "Image too wide, cropping width"
			img.crop(0, 0, 4096, height)
			img.save(filename=file)

		else:
			print "image is less than 4096px wide, saving"
			img.save(filename=file)



# uploads the image to S3 and deletes from the server
def upload_to_s3(file, dest):

	import os, tinys3, string, boto3, botocore
	from globe import app

	s3 = boto3.client(
   		"s3",
   		aws_access_key_id=os.environ['S3_PUB_KEY'],
   		aws_secret_access_key=os.environ['S3_PRIVATE_KEY']
	)

	print "dir: %s" % dest

	try:
		s3.upload_fileobj(
			file,
			os.environ['S3_BUCKET_NAME'],
			#TO DO: modify this param to use the correct path, as the above only takes the bucket name, need to add /static/user_... etc
			file.filename,
			ExtraArgs={
				"ACL": "public-read",
				"ContentType": file.content_type
			}
		)

	except Exception as e:
		# This is a catch all exception, edit this part to fit your needs.
		print("Something Happened: ", e)
		return e

	print "URL: " + os.environ['S3_ENDPOINT'] + "/" + os.environ['S3_BUCKET_NAME'] + "{}{}".format(dest, file.filename)
	return True

	'''try:
		#init conection to S3
		conn = tinys3.Connection(os.environ['S3_PUB_KEY'], os.environ['S3_PRIVATE_KEY'], tls=True, endpoint=os.environ['S3_ENDPOINT'])

		f = open(src, 'rb')

		conn.upload(directory, f, os.environ['S3_BUCKET_NAME'])

		print 'image has been uploaded to :%s' % directory
		print ", deleting local copy"
		return True

	except:
		print "failed"
		return False
'''


def delete(file):
	try:
		os.remove(file)
	except:
		print 'could not delete file: %s' % file
