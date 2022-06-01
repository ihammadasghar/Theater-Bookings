from datetime import date, datetime
from sqlite3 import Date
from flask import Blueprint, redirect, render_template, request
from .controllers import SeatController  as sctlr
from .controllers import ShowController as showctlr
from .controllers import ReservationController as rctlr
from .controllers import UserController as userctlr

views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def home():
    seats = sctlr.get_all()
    if not seats:
        sctlr.generate_seats()
        seats = sctlr.get_all()
        
    seat_letters = ["K", "J", "I", "H", "G", "F","--", "E", "D", "C", "B","--", "A"]
    return render_template("home.html", seat_letters=seat_letters, seats=seats, user=userctlr.get_logged_in_user())


@views.route('/reserve/<show_id>/<seat_id>', methods=['POST', 'GET'])
def create_reservation(show_id, seat_id):
    if request.method == "GET":
        show = showctlr.get(show_id)
        seat = sctlr.get(seat_id)
        return render_template("create_reservation.html", show=show, seat=seat)

    rctlr.create(1, seat_id, show_id)
    return redirect("/profile", user=userctlr.get_logged_in_user())


@views.route('/profile', methods=['POST', 'GET'])
def profile():
    return render_template("profile.html", user=userctlr.get_logged_in_user())


@views.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        if userctlr.login(name, email):
            return redirect("/")
        return render_template("login.html")
    return render_template("login.html", user=userctlr.get_logged_in_user())


@views.route('/logout', methods=['GET'])
def logout():
    userctlr.logout()
    return redirect("/")


@views.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        userctlr.create(name, email)
        userctlr.login(name, email)
        return redirect("/")
    return render_template("register.html", user=userctlr.get_logged_in_user())


@views.route('/show/<show_id>', methods=['POST', 'GET'])
def show_details(show_id):
    show = showctlr.get(show_id)
    return render_template("show_details.html", show=show, user=userctlr.get_logged_in_user())


@views.route('/search/<search_word>', methods=['POST', 'GET'])
def search_results(search_word):
    results = showctlr.search(search_word)
    return render_template("search_results.html", results=results, user=userctlr.get_logged_in_user())


@views.route('/shows/add', methods=['POST', 'GET'])
def add_show():
    if request.method == "POST":
        name = str(request.form["name"])
        description = str(request.form["description"])
        genre = str(request.form["genre"])
        date = datetime.strptime(str(request.form["date"]), '%Y-%m-%d')
        duration = int(request.form["duration"])
        time = datetime.strptime(request.form["time"], '%H:%M').time()
        showctlr.create(name, date, genre, duration, description, time)
    else:
        pass
    return render_template("add_show.html", user=userctlr.get_logged_in_user())
