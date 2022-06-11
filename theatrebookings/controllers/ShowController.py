from ..models import Show, Screening
from .. import db

# db functions syntax:
# db.session.add(item) create item
# db.session.delete(item) delete item
# db.session.commit() save changes NOTE: Use this after any changes to the db

# Show functions syntax:
# Find show with id: Show.query.get(id)
# Get list of all shows: Show.query.all()
# more examples of querying ways: https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/

### FUNCTIONS THAT INTERACT WITH OUR SHOWS AND SCREENING MODELS IN THE DATABASE ###

def create(name, genre, duration, description, img):
    shw = Show(name, genre, duration, description, img)
    db.session.add(shw)
    db.session.commit()
    return True


def delete(id):
    shw = Show.query.get(id)
    db.session.delete(shw)
    db.session.commit()
    return True


def update(id, name, genre, duration, description,img):
    show = Show.query.get(id)
    show.name = name
    show.genre = genre
    show.duration = duration
    show.description = description
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


def search(search_word):
    # TODO: search all the shows with names starting with "search"
    return Show.query.filter(Show.name.startswith(search_word)).all()


#screenings
def add_screening(show_id, datetime):
    screening = Screening(show_id, datetime)
    db.session.add(screening)
    db.session.commit()
    return True


def get_screening(screening_id):
    screening = Screening.query.get(screening_id)
    return screening


def delete_screening(screening_id):
    screening = get_screening(screening_id)
    db.session.delete(screening)
    db.session.commit()
    return True


def get_screenings(show_id):
    show = get(show_id)
    return show.screenings


def get_reserved_seats_ids(screening_id):
    screening = get_screening(screening_id)
    seat_ids = [res.seat_id for res in screening.reservations]
    return seat_ids