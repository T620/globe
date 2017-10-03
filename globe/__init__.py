import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)

db = SQLAlchemy(app)

print db

import globe.models
import globe.views
