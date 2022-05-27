from models import Shows
from .. import db

# db functions syntax:
# db.session.add(item) create item
# db.session.delete(item) delete item
# db.session.commit() save changes NOTE: Use this after any changes to the db

# Show functions syntax:
# Find show with id: Show.query.get(id)
# Get list of all shows: Show.query.all()
# more examples of querying ways: https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/

def create(name, date, genre, duration, description, time):
    # TODO: get information about show in parameters, make a show object and save it in the data base 
    pass


def delete(id):
    # TODO: get show id in parameter, find the show using query and delete it from the database 
    pass 


def get(id):
    # TODO: get show id as a parameter, find the show using query and return the show 
    pass


def get_first(num):
    # TODO: get first "num" shows from the database and return them as a list
    pass


def search(search):
    # TODO: search all the shows with names starting with "search"
    pass