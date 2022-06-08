from datetime import date, datetime
import re
from sqlite3 import Date
from flask import Blueprint, redirect, render_template, request
from .controllers import SeatController  as seatctlr
from .controllers import ShowController as showctlr
from .controllers import ReservationController as reservationctlr
from .controllers import UserController as userctlr

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home(): 
    if request.method == "GET":
        shows = showctlr.get_first(10)
    return render_template("home.html",shows=shows, user=userctlr.get_logged_in_user())


# User views
@views.route('/reservations', methods=['GET'])
def reservations():
    #  Check if a user is logged in
    user = userctlr.get_logged_in_user()
    if not user:
        return redirect('/login')

    reservations = reservationctlr.get_user_reservations(user.id)

    reservation_details = []
    for res in reservations:
        id = res.id
        screening = showctlr.get_screening(res.screening_id)
        show = showctlr.get(screening.id)
        seat = seatctlr.get(res.seat_id)

        reservation_details.append((id, screening, show, seat))

    return render_template("reservations.html", reservation_details=reservation_details, user=user)


@views.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        if userctlr.login(name, email):
            return redirect("/")
        
        message = "Incorrect name or email"
        return render_template("login.html", message=message, user=userctlr.get_logged_in_user())
    return render_template("login.html", message=None, user=userctlr.get_logged_in_user())


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


# Show views
@views.route('/shows/<show_id>', methods=['POST', 'GET'])
def show_details(show_id):
    show = showctlr.get(show_id)
    screenings = showctlr.get_screenings(show_id)

    return render_template("show_details.html", show=show, screenings=screenings, user=userctlr.get_logged_in_user())


@views.route('/search', methods=['POST', 'GET'])
def search_results():
    if request.method == "POST":
        search_word = str(request.form["search_word"])
        results = showctlr.search(search_word)

    return render_template("search.html", results=results, user=userctlr.get_logged_in_user())


@views.route('/shows/add', methods=['POST', 'GET'])
def add_show():
    if request.method == "POST":
        name = str(request.form["name"])
        description = str(request.form["description"])
        genre = str(request.form["genre"])
        duration = int(request.form["duration"])
        img_link = str(request.form["img"])
        showctlr.create(name, genre, duration, description, img_link)
    
    return render_template("add_show.html", user=userctlr.get_logged_in_user())


@views.route('/shows/screenigs/add/<show_id>', methods=['POST', 'GET'])
def add_screening(show_id):
    if request.method == "POST":
        date = str(request.form["date"])
        time = str(request.form["time"])
        dateandtime = date + " " + time
        dateandtime = datetime.strptime(dateandtime, '%Y-%m-%d %H:%M')
        showctlr.add_screening(show_id,dateandtime)
        return redirect(f'/shows/{show_id}')
    
    show = showctlr.get(show_id)
    return render_template("add_screening.html",show=show, user=userctlr.get_logged_in_user())
    

@views.route('/screenings/<screening_id>', methods=['POST', 'GET'])
def screening_details(screening_id):
    screening = showctlr.get_screening(screening_id)
    show = showctlr.get(screening.show_id)
    seats = seatctlr.get_all()
    reserved_seat_ids = showctlr.get_reserved_seats_ids(screening_id)

    #  In case the database was just created
    if not seats:
        seatctlr.generate_seats()
        seats = seatctlr.get_all()
    
    seat_letters = ["K", "J", "I", "H", "G", "F","--", "E", "D", "C", "B","--", "A"]
    return render_template("screening_details.html", show=show, seat_letters=seat_letters, seats=seats, screening=screening, reserved_seat_ids=reserved_seat_ids, user=userctlr.get_logged_in_user())



@views.route('/reservations/<screening_id>/<seat_id>', methods=['POST', 'GET'])
def create_reservation(screening_id, seat_id):
    #  Check if a user is logged in
    user = userctlr.get_logged_in_user()
    if not user:
        return redirect('/login')

    if request.method == "POST":
       reservationctlr.create(user.id, screening_id, seat_id)
       return redirect('/')
    
    screening = showctlr.get_screening(screening_id)
    show = showctlr.get(screening.show_id)
    seat = seatctlr.get(seat_id)
    return render_template("create_reservation.html", screening=screening, show=show, seat=seat, user=user)


@views.route('/reservations/delete/<reservation_id>/', methods=['GET'])
def delete_reservation(reservation_id):
    reservationctlr.delete(reservation_id)
    return redirect('/reservations')
