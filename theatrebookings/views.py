from email import message
from flask import Blueprint, render_template, request, flash, jsonify
from .models import User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def home():
    message = [1,2,3]
    return render_template("home.html", message=message)


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