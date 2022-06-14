import imp
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint

db = SQLAlchemy()  #  Sqlalchemy database object/instance
DB_NAME = "database.db"
logged_in_user = None  #  Stores the currently logged in user info 
views = Blueprint('views', __name__)