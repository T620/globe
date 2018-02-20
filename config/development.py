import os

class Development():
	print "[INFO] Starting environment in Development"
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	DEBUG=True
	DEVELOPMENT=True
	BCRYPT_LOG_ROUNDS = 5
	FLASK_DEBUG=1
	DATABASE_URL=os.environ['DATABASE_URL']
	APP_SECRET_KEY="dev"
	MAIL_USERNAME="josh.tait3@gmail.com"
	MAIL_PASSWORD=os.environ['MAIL_PASSWORD']
	MAPS_API_KEY=os.environ['MAPS_API_KEY']
	S3_PUB_KEY=os.environ['S3_PUB_KEY']
	S3_PRIVATE_KEY=os.environ['S3_PRIVATE_KEY']
