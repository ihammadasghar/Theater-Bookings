from ..models import Show
from .. import db

# db functions syntax:
# db.session.add(item) create item
# db.session.delete(item) delete item
# db.session.commit() save changes NOTE: Use this after any changes to the db

# Show functions syntax:
# Find show with id: Show.query.get(id)
# Get list of all shows: Show.query.all()
# more examples of querying ways: https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/

def create(name, date, genre, duration, description, time, img):
    shw = Show(name,date,genre,duration,description,time,img)
    db.session.add(shw)
    db.session.commit()
    return True


def delete(id):
    shw = Show.query.get(id)
    db.session.delete(shw)
    db.session.commit()
    return True


def update(name, date, genre, duration, description, time, id,img):
    show = Show.query.get(id)
    show.name = name
    show.date = date
    show.genre = genre
    show.duration = duration
    show.description = description
    show.time = time
    show.img = img
    db.session.commit()
    return True


def get(id):
    # TODO: get show id as a parameter, find the show using query and return the show 
    shw = Show.query.get(id)
    Show.query.get(id)
    return shw


def get_reservations(id):
    shw = Show.query.get(id)
    return shw.reservations


def get_first(num):
    # TODO: get first "num" shows from the database and return them as a list
    shws = Show.query.order_by(Show.id).all()
    first_num = shws[:num]
    return first_num


def search(search):
    # TODO: search all the shows with names starting with "search"
    return Show.query.filter_by(Show.name.startswith(search)).all()


def get_reserved_seats_ids(id):
    show = get(id)
    seat_ids = [res.seat_id for res in show.reservations]
    return seat_ids