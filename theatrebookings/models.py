from .settings import db

### MODEL DEFINITIONS AND RELATIONAL DATABASE STRUCTURE ###

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    reservations = db.relationship('Reservation')  # 1 user has many reservations

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(3))
    vip = db.Column(db.Boolean)
    reservations = db.relationship('Reservation')  # 1 seat has many reservations
    price = db.Column(db.Float)
    
    def __init__(self, position: str, vip: bool, price: float) -> None:
        self.position = position
        self.vip = vip
        self.price = price


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    description = db.Column(db.String(150))
    img_link = db.Column(db.String(500))
    screenings = db.relationship('Screening')

    def __init__(self, name: str, genre: str, duration: int, description: str, img_link: str) -> None:
        self.name = name
        self.genre = genre
        self.duration = duration
        self.description = description
        self.img_link = img_link


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'))   # 1 reservation has 1 seat
    screening_id = db.Column(db.Integer, db.ForeignKey('screening.id'))   # 1 reservation has 1 screening
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # i reservation has 1 user

    def __init__(self, user_id: int, seat_id: int, screening_id: int) -> None:
        self.user_id = user_id
        self.seat_id = seat_id
        self.screening_id = screening_id


class Screening(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))   # 1 screening has 1 show
    datetime = db.Column(db.DateTime(timezone=True))
    reservations = db.relationship('Reservation')  # 1 screening has many reservations

    def __init__(self, show_id, datetime) -> None:
        self.show_id = show_id
        self.datetime = datetime