import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import flask_whooshalchemy as whooshalchemy


app = Flask(__name__)

#load the default settings
app.config.from_envvar("APP_CONFIG_FILE")
print os.environ['APP_CONFIG_FILE']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
mail = Mail(app)


import globe.models
import globe.views
