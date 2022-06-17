from flask import redirect, render_template, request
from ..controllers import ShowController as showctlr
from ..controllers import SeatController as seatctlr
from ..controllers import ReservationController as reservationctlr
from ..controllers import UserController as userctlr
from ..settings import views

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

    #  Check if the user is logged in and the user is admin
    if not user:
        return redirect("/login")

    if not user.name == "Admin":
        return redirect("/login")

    day, month, year = 0,0,0

    if request.method == "POST":
        # Get html form data and for date
        day = int(request.form["day"])
        month = int(request.form["month"])
        year = int(request.form["year"])

    data = reservationctlr.filter(day, month, year)
    
    # Render the register page on GET request
    return render_template("sales.html", data=data, date=f"{day}/{month}/{year}", user=user)


@views.route('/admin/database', methods=['GET'])
def database():
    user=userctlr.get_logged_in_user()

    #  Check if the user is logged in and the user is admin
    if not user:
        return redirect("/login")

    if not user.name == "Admin":
        return redirect("/login")

    #  get all the data from the database
    users = userctlr.get_all()
    shows = showctlr.get_all()
    screenings = showctlr.get_all_screenings()
    screenings = [(s, showctlr.get(s.show_id)) for s in screenings]
    res = reservationctlr.get_all()
    reservations = []
    for r in res:
        pos = seatctlr.get(r.seat_id).position
        screening = showctlr.get_screening(r.screening_id)
        show_name = showctlr.get(screening.show_id).name
        user_name = userctlr.get(r.user_id).name
        reservations.append((r.id, pos, screening, show_name, user_name))
    
    # Render the register page on GET request
    return render_template("database.html", users=users, shows=shows, screenings=screenings, reservations=reservations, user=user)