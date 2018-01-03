import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message


app = Flask(__globe__)

#load the default settings
app.config.from_pyfile("../config/secrets.py")



db = SQLAlchemy(app)
mail = Mail(app)

print db

import globe.models
import globe.views
