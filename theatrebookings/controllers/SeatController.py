from ..database import db
from ..models import Seat

def generate_seats():
    a = {"K": 14, "J": 14, "I": 14, "H": 14, "G": 14, "F": 8,"E": 14, "D": 14, "C": 14, "B": 14,"A": 8}
    for letter, num in a.items():
        for i in range(1, num+1):
            position = letter + str(i)
            vip = False
            price = 4.00
            if num == 8 and num in [3, 4, 5, 6]:
                vip = True
                price = 12.00
            seat = Seat(position, vip, price)
            db.session.add(seat)
    db.session.commit()


def get_all():
    return Seat.query.all()