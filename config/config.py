#SECRETS

print "[INFO] Env config vars loaded"

#DATABASE_URL is defined in the environment of the machine running the app
#for instance, if running locally, DATABASE_URL is set doing:
#export DATABASE_URL="psql://epb/" etc

#for the time being
DEBUG=True
DEVELOPMENT=True
BCRYPT_LOG_ROUNDS = 5
SQLALCHEMY_TRACK_MODIFICATIONS=False

#so secure lol
SECRET_KEY="dev"
#FLASK_DEBUG=Heroku

print "[INFO] Dev Mode=%s" % DEVELOPMENT
