import os
import secrets

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
# Never hardcode the key - set SECRET_KEY in the environment for any real deployment
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manger = LoginManager(app)
login_manger.login_view = 'login_page'
login_manger.login_message_category = 'info'

from market import routes