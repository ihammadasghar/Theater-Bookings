from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  #  Sqlalchemy database object/instance
DB_NAME = "database.db"
logged_in_user = None  #  Stores the currently logged in user info 