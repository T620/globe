#handles file uploads from the user
from werkzeug.utils import secure_filename
import os
from globe import app
from flask import session

allowedExtensions= set(['jpg', 'jpeg', 'png'])

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in allowedExtensions


def save(file, directory):
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		print 'saved file, cropping...'
		os.makedirs(directory)
		directory = os.path.join(directory, filename)

		try:
			file.save(directory)
			print directory
			return True
		except:
			return False
		#this last step creates the absolute full path for image magick to open the file from the saved dest.




# annoyingly, magick needs the image saved to a disk first.
def crop(file):
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
			img.save(filename=file)
			return True

		else:
			print "image is less than 4096px wide, saving"
			img.save(filename=file)
			return True



# uploads the image to S3 and deletes from the server
def upload_to_s3(directory, url):
	import os, tinys3, string
	from globe import app

	#init conection to S3
	conn = tinys3.Connection(os.environ['S3_PUB_KEY'], os.environ['S3_PRIVATE_KEY'], tls=True)
	f = open(directory, 'rb')

	try:
		conn.upload(url, f, os.environ['S3_BUCKET_NAME'])
		print 'image has been uploaded to :%s' % url
		print ", deleting local copy"
		return True
	except:
		print "failed to uploadimage"
		return False



def delete(file):
	try:
		os.remove(file)
	except:
		print 'could not delete file: %s' % file
