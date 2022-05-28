from flask import Blueprint, render_template, request, flash, jsonify
from .controllers import SeatController  as sctlr

views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def home():
    seats = sctlr.get_all()
    if not seats:
        sctlr.generate_seats()
        seats = sctlr.get_all()
        
    seat_letters = ["K", "J", "I", "H", "G", "F","--", "E", "D", "C", "B","--", "A"]
    return render_template("home.html", seat_letters=seat_letters, seats=seats)


@views.route('/reservations', methods=['POST', 'GET'])
def reservations():
    return render_template("reservations.html")


@views.route('/reserve', methods=['POST', 'GET'])
def create_reservation():
    return render_template("create_reservation.html")


@views.route('/edit/reservation', methods=['POST', 'GET'])
def edit_reservation():
    return render_template("edit_reservation.html")


@views.route('/profile', methods=['POST', 'GET'])
def profile():
    return render_template("profile.html")


@views.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")


@views.route('/register', methods=['POST', 'GET'])
def register():
    return render_template("register.html")