from models import Seat
from datetime import datetime

class Reservation:
    def __init__(self, user: str, seat: Seat, date: datetime) -> None:
        self.user = user
        self.seat = seat
        self.date = date
    
    