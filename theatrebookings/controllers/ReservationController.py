from models import Reservation
from .. import db

# db functions syntax:
# db.session.add(item) create item
# db.session.delete(item) delete item
# db.session.commit() save changes NOTE: Use this after any changes to the db

# Reservation functions syntax:
# Find reservation with id: Reservation.query.get(id)
# Get list of all reservations: Reservation.query.all()
# more examples of querying ways: https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/

def create():
    # TODO: get information about reservation in parameters, make a reservation object and save it in the data base 
    pass


def delete():
    # TODO: get reservation id in parameter, find the reservation using query and delete it from the database 
    pass 


def update():
    # TODO: get new information about reservation in parameters and reservation id, find the reservation using query and update it in the database 
    pass


def get():
    # TODO: get reservation id as a parameter, find the reservation using query and return the reservation 
    pass


def get_reservation_reservations():
    # TODO: get reservation_id as a parameter, get all the reservations of the reservation from the database and return them as a list
    pass