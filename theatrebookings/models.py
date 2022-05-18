from . import db
from sqlalchemy.sql import func
import datetime
import time


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, position: str, vip: bool, price: float) -> None:
        self.position = position
        self.vip = vip
        self.price = price


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user: str, seat: Seat, date: datetime) -> None:
        self.user = user
        self.seat = seat
        self.date = date


class Shows(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, name: str, date: datetime, genre: str, duration: int, description: str, time: time) -> None:
        self.name = name
        self.genre = genre
        self.duration = duration
        self.date = date
        self.description = description
        self.time = time