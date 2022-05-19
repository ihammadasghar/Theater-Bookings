from . import db
from sqlalchemy.sql import func
import datetime
import time


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    reservations = db.relationship('Note')

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(3))
    vip = db.Column(db.Boolean)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'))
    
    def __init__(self, position: str, vip: bool, price: float) -> None:
        self.position = position
        self.vip = vip
        self.price = price


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True))
    description = db.Column(db.String(150))
    reservations = db.relationship('Reservation')

    def __init__(self, name: str, date: datetime, genre: str, duration: int, description: str, time: time) -> None:
        self.name = name
        self.genre = genre
        self.duration = duration
        self.date = date
        self.description = description


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'))
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True))

    def __init__(self, user_id: int, seat: Seat, show: Show) -> None:
        self.user_id = user_id
        self.seat = seat
        self.show = show
