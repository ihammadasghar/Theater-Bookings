from ..models import User
from .. import db
from .. import logged_in_user

# db functions syntax:
# db.session.add(item) create item
# db.session.delete(item) delete item
# db.session.commit() save changes NOTE: Use this after any changes to the db

# User functions syntax:
# Find user with id: User.query.get(id)
# Get list of all users: User.query.all()
# more examples of querying ways: https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/

### FUNCTIONS THAT INTERACT WITH OUR USER MODEL IN THE DATABASE ###

def create(name, email):
    user = User(name, email)
    db.session.add(user)
    db.session.commit()
    return True


def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return True


def update(new_name, new_email, id):
    user = User.query.get(id)
    user.name = new_name
    user.email = new_email
    db.session.commit()
    return True


def get(id):
    user =  User.query.get(id)
    return user


def get_all():
    user = User.query.all()
    return user


def login(name, email):
    user = User.query.filter_by(name=name, email=email).first()
    if user:
        global logged_in_user 
        logged_in_user = user
        return True
    return False


def logout():
    global logged_in_user 
    logged_in_user = None


def get_logged_in_user():
    return logged_in_user