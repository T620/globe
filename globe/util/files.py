#handles file uploads from the user
from werkzeug.utils import secure_filename
import os
from globe import app
from flask import session

def file_allowed(filename, allowedExtensions):
	#check the user isn't doing anything fishy by checking the file extension
	return "." in filename and filename.rsplit('.', 1)[1] in allowedExtensions


def save(file, folder):
	#check the file has an allowed extension first
	allowedExtensions = set(['jpeg', 'jpg', 'png'])

	if file.filename != '':
		if file_allowed(file.filename, allowedExtensions):
			file.save(folder)
			print 'saved file to: %s' % folder


def modify(file, folder, name):
	#do some magik
	from wand.image import Image

	#convert image to jpg format
	print folder
	with Image(filename=folder) as img:
		img.format = 'jpeg'
		#save again
		if name == "cover":
			img.crop(1920, 300)
		else:
			img.crop(250, 250)
		subfolder = session['user'] + '/profile/' + name +".jpeg"
		folder = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
		img.save(filename=folder)


def delete(file):
	os.remove(file)
