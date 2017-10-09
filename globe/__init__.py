import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)

#load the default settings first
app.config.from_pyfile("../config/config.py")
#load the secrets
app.config.from_envvar('APP_CONFIG_FILE')

db = SQLAlchemy(app)


import globe.models

print db

import globe.views
