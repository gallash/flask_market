# One can import variables from this __init__ file, it seems

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# New way of creating a database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Creating and configuring the Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SECRET_KEY"] = "437d992fe280143928990ebc"  # Necessary for the CSRF. Why? Why can't I simply put `os.urandom(12).hex()` here?

db.init_app(app)
bcrypt = Bcrypt(app)  # Creates hash passwords instead of saving them as plain text

login_manager = LoginManager(app)
login_manager.login_view = "login_page"  # Simply pass in the name of the view
login_manager.login_message = "Please log in to access this page"
login_manager.login_message_category = "info"


from market import routes, models
