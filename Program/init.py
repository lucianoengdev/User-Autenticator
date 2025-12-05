from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, "users.db")
app.config['SECRET_KEY'] = '123456'


db = SQLAlchemy(app)

from .models import User




from Program import forms
from Program import routes


if __name__ == "__main__":
    app.run(debug=True)