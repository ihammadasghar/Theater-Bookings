from datetime import datetime
from flask import redirect, render_template, request
from ..controllers import SeatController  as seatctlr
from ..controllers import ShowController as showctlr
from ..controllers import UserController as userctlr
from ..settings import views


### SHOW VIEWS ###
@views.route('/shows/<show_id>', methods=['GET'])
def show_details(show_id):
    user=userctlr.get_logged_in_user()
    #  Check if the user is logged in 
    if not user:
        return redirect("/login")
        
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
    user=userctlr.get_logged_in_user()
    #  Check if the user is logged in and the user is admin
    if not user:
        return redirect("/login")

    if not user.name == "Admin":
        return redirect("/login")

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
    return render_template("add_show.html", user=user)


@views.route('/shows/delete/<show_id>', methods=['GET'])
def delete_show(show_id):
    showctlr.delete(show_id)
    return redirect('/')


### SCREENING VIEWS ###
@views.route('/screenings/add/<show_id>', methods=['POST', 'GET'])
def add_screening(show_id):
    user=userctlr.get_logged_in_user()
    #  Check if the user is logged in and the user is admin
    if not user:
        return redirect("/login")

    if not user.name == "Admin":
        return redirect("/login")

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
    return render_template("add_screening.html", show=show, user=user)
    
@views.route('/screening/delete/<screening_id>', methods=['GET'])
def delete_screening(screening_id):
    showctlr.delete_screening(screening_id)
    return redirect('/')
    

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
