from datetime import datetime
from email import message
from flask import Blueprint, redirect, render_template, request
from .controllers import SeatController  as seatctlr
from .controllers import ShowController as showctlr
from .controllers import ReservationController as reservationctlr
from .controllers import UserController as userctlr

views = Blueprint('views', __name__)

### MAIN VIEWS ###
@views.route('/', methods=['GET'])
def home(): 
    #  Pass information about 10 shows to the home page
    shows = showctlr.get_first(9)
    return render_template("home.html", shows=shows, user=userctlr.get_logged_in_user())


### USER VIEWS ###
@views.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        # Get information given by the user in the html form
        name = request.form["name"]
        email = request.form["email"]

        # Redirect to home if logged in successfully
        if userctlr.login(name, email):
            return redirect("/")
        
        # Else rerender the login page with a error message
        message = "Incorrect name or email"
        return render_template("login.html", message=message, user=userctlr.get_logged_in_user())
    
    # render the login page in case of a GET request
    return render_template("login.html", message=None, user=userctlr.get_logged_in_user())


@views.route('/logout', methods=['GET'])
def logout():
    # Logout the user and redirect to home
    userctlr.logout()
    return redirect("/")


@views.route('/register', methods=['POST', 'GET'])
def register():
    message = None

    if request.method == "POST":
        # Get html form data and register the user
        name = request.form["name"]
        email = request.form["email"]
        if userctlr.name_exists(name):
            message = f"A user with the name '{name}' already exists"
        elif userctlr.email_exists(email):
            message = f"This email has already been registered"
        else:
            userctlr.create(name, email)
            userctlr.login(name, email)
            return redirect("/")
    
    # Render the register page on GET request
    return render_template("register.html", message=message, user=userctlr.get_logged_in_user())


@views.route('/admin/sales', methods=['POST', 'GET'])
def sales():
    user=userctlr.get_logged_in_user()
    # if not user.name == "Admin":
    #     return redirect("/")

    day, month, year = 0,0,0

    if request.method == "POST":
        # Get html form data and register the user
        day = int(request.form["day"])
        month = int(request.form["month"])
        year = int(request.form["year"])

    data = reservationctlr.filter(day, month, year)
    
    # Render the register page on GET request
    return render_template("sales.html", data=data, date=f"{day}/{month}/{year}", user=user)


### SHOW VIEWS ###
@views.route('/shows/<show_id>', methods=['GET'])
def show_details(show_id):
    #  Get the show throught the show id in the url and its screenings and pass it to the page
    show = showctlr.get(show_id)
    screenings = showctlr.get_screenings(show_id)
    return render_template("show_details.html", show=show, screenings=screenings, user=userctlr.get_logged_in_user())


@views.route('/search', methods=['POST'])
def search_results():
    # Get the seach word from the html form and get the results and pass them to the page
    search_word = str(request.form["search_word"])
    results = showctlr.search(search_word)
    return render_template("search.html", results=results, user=userctlr.get_logged_in_user())


@views.route('/shows/add', methods=['POST', 'GET'])
def add_show():
    if request.method == "POST":
        #  Get the data from the html form and create a show
        name = request.form["name"]
        description = request.form["description"]
        genre = request.form["genre"]
        duration = int(request.form["duration"])
        img_link = request.form["img"]
        showctlr.create(name, genre, duration, description, img_link)
        return redirect('/')
    
    # Render the add show page with the html form
    return render_template("add_show.html", user=userctlr.get_logged_in_user())


@views.route('/shows/delete/<show_id>', methods=['GET'])
def delete_show(show_id):
    showctlr.delete(show_id)
    return redirect('/')


### SCREENING VIEWS ###
@views.route('/screenings/add/<show_id>', methods=['POST', 'GET'])
def add_screening(show_id):
    if request.method == "POST":
        #  Get the data from the html form and create a screening
        date = str(request.form["date"])
        time = str(request.form["time"])
        dateandtime = date + " " + time
        dateandtime = datetime.strptime(dateandtime, '%Y-%m-%d %H:%M')
        showctlr.add_screening(show_id,dateandtime)
        return redirect(f'/shows/{show_id}')
    
    #  Get show of the show id in the url and render add screening form page 
    show = showctlr.get(show_id)
    return render_template("add_screening.html", show=show, user=userctlr.get_logged_in_user())
    

@views.route('/screenings/<screening_id>', methods=['GET'])
def screening_details(screening_id):
    # Get the screening with screening_id in the url and its show
    screening = showctlr.get_screening(screening_id)
    show = showctlr.get(screening.show_id)

    # Get all the seats to show the hall seat layout
    seats = seatctlr.get_all()
    reserved_seat_ids = showctlr.get_reserved_seats_ids(screening_id)

    #  In case the database was just created create all the seats
    if not seats:
        seatctlr.generate_seats()
        seats = seatctlr.get_all()
    
    # Letters required by the html table to make the hall seat layout
    seat_letters = ["K", "J", "I", "H", "G", "F","--", "E", "D", "C", "B","--", "A"]

    return render_template("screening_details.html", show=show, seat_letters=seat_letters, seats=seats, screening=screening, reserved_seat_ids=reserved_seat_ids, user=userctlr.get_logged_in_user())


### RESERVATION VIEWS ###
@views.route('/reservations', methods=['GET'])
def reservations():
    #  Check if a user is logged in
    user = userctlr.get_logged_in_user()
    if not user:
        return redirect('/login')

    # Get user reservation and collect all the details about resevation's screening, show and seat to pass to the page
    reservations = reservationctlr.get_user_reservations(user.id)
    reservation_details = []

    for res in reservations:
        id = res.id
        screening = showctlr.get_screening(res.screening_id)
        show = showctlr.get(screening.show_id)
        seat = seatctlr.get(res.seat_id)
        reservation_details.append((id, screening, show, seat))

    return render_template("reservations.html", reservation_details=reservation_details, user=user)


@views.route('/reservations/<screening_id>/<seat_id>', methods=['POST', 'GET'])
def create_reservation(screening_id, seat_id):
    #  Check if a user is logged in
    
    user = userctlr.get_logged_in_user()
    if not user:
        return redirect('/login')

    if request.method == "POST":
        # Create a new reservation using the ids the url and logged in user id
        reservationctlr.create(user.id, screening_id, seat_id)
        return redirect('/reservations')
    
    # GET request
    # Get the screening, show and seat to render the confirmation page 
    screening = showctlr.get_screening(screening_id)
    show = showctlr.get(screening.show_id)
    seat = seatctlr.get(seat_id)
    return render_template("create_reservation.html", screening=screening, show=show, seat=seat, user=user)


@views.route('/reservations/delete/<reservation_id>', methods=['GET'])
def delete_reservation(reservation_id):
    # Delete the reservation with the id in the url
    reservationctlr.delete(reservation_id)
    return redirect('/reservations')


@views.route('/reservations/edit/<reservation_id>', methods=['POST', 'GET'])
def edit_reservation(reservation_id):
    #  Get all the information about the reservation from the database
    user = userctlr.get_logged_in_user()
    reservation = reservationctlr.get(reservation_id)
    old_seat = seatctlr.get(reservation.seat_id) 
    screening = showctlr.get_screening(reservation.screening_id)
    show = showctlr.get(screening.show_id)
    reserved_seat_ids = showctlr.get_reserved_seats_ids(screening.id)

    error_message = None

    if request.method == "POST":
        #  Get information about the new seat
        seat_pos = request.form['seat_number'].upper()
        new_seat = seatctlr.get_by_position(seat_pos)
        
        # Validations
        #  Check if the new seat exits
        if new_seat:
            #  Check if its not already reserved
            if new_seat.id not in reserved_seat_ids:
                # Update the reservation
                reservationctlr.update(reservation.id, user.id, new_seat.id, screening.id)
                return redirect('/reservations')

            error_message = f"{new_seat.position} is already reserved"

        else:
            error_message = f"No seat with number {seat_pos}"

        # If the reservation is not updated because of the validations, the page will be rerendered with a error message

    # Letters required by the html table to make the hall seat layout
    seat_letters = ["K", "J", "I", "H", "G", "F","--", "E", "D", "C", "B","--", "A"]
    seats = seatctlr.get_all()

    return render_template("edit_reservation.html", 
                            reservation=reservation, 
                            screening=screening,
                            show=show,
                            seat=old_seat,
                            seat_letters=seat_letters, 
                            seats=seats, 
                            reserved_seat_ids=reserved_seat_ids,
                            error_message=error_message,
                            user=user)