## Topics:
- [Overview](#Overview)
- [Setup](#Setting-up)
- [How to contribute](#Adding-a-feature-to-the-project)

## Introduction:
The Theatre-booking project uses mainly the following tecnologies:
- Python
- Html
- Flask (python library to help design a webapp)
- Flask SqlAlchemy (library to help manage the database)

The project use the mvc architecture.
### Models:
We have defined the structure of our relational database as well as the structure of the classes we will use through out the project (models.py).
Classes: User, Show, Reservation, Seat

### Controllers:
We 4 different contollers each to manage and manipulate the data of all the different classes defined in the model.
controllers: UserController, ShowController, ReservationController, SeatController

### Views:
Our views.py module, acts as a connection between the html pages and our backend (Flask/Python), In each view function has a specific address and the methods http requests it is allowed to accept (on top of each function).
We use the controller functions in the views to prepare information to sent to be displayed on the html pages (GET METHOD) and to be recieve information from the html pages and process it using our controller functions and manipulate the database (POST METHOD).

## Setting up:
1. Clone the Repository
```
git clone https://github.com/ihammadasghar/Theatre-Bookings.git
```
2. cd to Theatre-Bookings and dowload all the required packages/libraries:
```
pip install -r requirements.txt
pip install flask_sqlalchemy
```
## Adding a feature to the project

1. Make a new branch with the your feature name
```
git pull origin main
git checkout -b branch_name
```
2. Add the changes to the code

3. Add and Commit
```
git add .
git commit -m "what changes you made"
```
4. Push your branch.
```
git pull origin main
git pull origin branch_name
git push origin branch_name
```
5. Go to github there will be a notification to "create a Pull request", add a description of the functionality of your feature for others to understand what you did and post the pull request.
