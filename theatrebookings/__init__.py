from flask import Flask
from os import path
from .settings import *

# Used every time the app is launched
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import User

    create_database(app)

    return app

#  Used to create the database following the structure defined in models.py
def create_database(app):
    # Only used when app is launched for the first time whend database doesn't exist
    if not path.exists('theatrebookings/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        return True
    return False