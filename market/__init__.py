from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '1380f60fb99eab38cf934e36'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manger = LoginManager(app)
login_manger.login_view = 'login_page'
login_manger.login_message_category = 'info'

from market import routes