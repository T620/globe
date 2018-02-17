import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message


app = Flask(__name__)

#load the default settings
app.config.from_pyfile("../config/config.py")

#config_name = os.getenv('FLASK_CONFIGURATION', 'default')
#app.config.from_object(config[config_name]) # object-based default configuration


db = SQLAlchemy(app)
mail = Mail(app)


import globe.models
import globe.views
