from flask import redirect, render_template, request
from ..controllers import SeatController  as seatctlr
from ..controllers import ShowController as showctlr
from ..controllers import ReservationController as reservationctlr
from ..controllers import UserController as userctlr
from ..settings import views

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

    # In case of quick reserve
    if seat_id == "quick":
        # Find the first seat that is not reserved
        reserved_seat_ids = showctlr.get_reserved_seats_ids(screening_id)
        NUM_SEATS = 142
        for i in range(1, NUM_SEATS):
            if i not in reserved_seat_ids:
                seat_id = i
                return redirect(f'/reservations/{screening_id}/{seat_id}')

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
