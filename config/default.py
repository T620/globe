import os

class Default():
	print "[INFO] Starting environment in Default/Development"
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
	S3_ENDPOINT='s3.us-west-2.amazonaws.com'
	S3_BUCKET_NAME='elasticbeanstalk-us-west-2-908893185885'
	S3_PUB_KEY=os.environ['S3_PUB_KEY']
	S3_PRIVATE_KEY=os.environ['S3_PRIVATE_KEY']
