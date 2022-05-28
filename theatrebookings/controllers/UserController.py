from models import Reservation, User
from .. import db


def create(name, email):
    # TODO: get information about user in parameters, make a user object and save it in the data base 
    user = User(name, email)
    db.session.add(user)
    db.session.commit()
    return True


def delete(id):
    # TODO: get user id in parameter, find the user using query and delete it from the database 
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return True




def update(new_name, new_email, id):
    # TODO: get new information about user in parameters and user id, find the user using query and update it in the database 
    user = User.query.get(id)
    user.name = new_name
    user.email = new_email
    db.session.commit()
    return True

def get(id):
    # TODO: get user id as a parameter, find the user using query and return the user 
    user =  User.query.get(id)
    return user


def get_all():
    # TODO: get all the users from the database and return them as a list
    user = User.query.all()
    return user