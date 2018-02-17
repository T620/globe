import os


def get_env():
	environment = os.environ['FLASK_CONFIGURATION']

	if environment == "development":
		return Development(Base)
	if environment == "production":
		return Production(Base)
	else:
		return Production(Base)


class Base(object):
	DEBUG = False
	FLASK_DEBUG=0
	TESTING = False
	SQLALCHEMY_TRACK_MODIFICATIONS=False

class Development(Base):
	print "[INFO] Starting environment in Development"
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	DEBUG=True
	DEVELOPMENT=True
	BCRYPT_LOG_ROUNDS = 5
	FLASK_DEBUG=1
	APP_CONFIG_FILE="/home/josh/projects/globe/config/config.py"
	DATABASE_URL=os.environ['DATABASE_URL']
	APP_SECRET_KEY="dev"
	MAIL_USERNAME="josh.tait3@gmail.com"
	MAIL_PASSWORD=os.environ['MAIL_PASSWORD']
	MAPS_API_KEY=os.environ['MAPS_API_KEY']
	S3_ENDPOINT='s3.us-west-2.amazonaws.com'
	S3_BUCKET_NAME='elasticbeanstalk-us-west-2-908893185885'
 	S3_PUB_KEY=os.environ['S3_PUB_KEY']
	S3_PRIVATE_KEY=os.environ['S3_PRIVATE_KEY']

class Production(Base):
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	DEBUG=False
	DEVELOPMENT=False
	BCRYPT_LOG_ROUNDS = 10
	DATABASE_URL=os.environ['DATABASE_URL']
	APP_SECRET_KEY=os.environ['APP_SECRET_KEY']
	MAIL_USERNAME="josh.tait3@gmail.com"
	MAIL_PASSWORD=os.environ['MAIL_PASSWORD']
	MAPS_API_KEY=os.environ['MAPS_API_KEY']
	S3_ENDPOINT='s3.us-west-2.amazonaws.com'
	S3_BUCKET_NAME='elasticbeanstalk-us-west-2-908893185885'
 	S3_PUB_KEY=os.environ['S3_PUB_KEY']
	S3_PRIVATE_KEY=os.environ['S3_PRIVATE_KEY']
