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

def create(user_id, seat_id, show_id, date):
    reservation = Reservation(user_id, seat_id, show_id, date)
    db.session.add(reservation)
    db.session.commit()
    return True


def delete(id):
    reservation = Reservation.query.get(id)
    db.session.delete(reservation)
    db.session.commit()
    return True


def update(user_id, seat_id, show_id, date):
    reservation = Reservation.query.get(id)
    reservation.user_id = user_id
    reservation.seat_id = seat_id
    reservation.show_id = show_id
    reservation.date = date
    db.session.commit()
    return True


def get():
    reservation = Reservation.query.get(id)
    return reservation