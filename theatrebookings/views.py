from flask import Blueprint, render_template, request, flash, jsonify
from .models import User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def home():
    message = [1,2,3]
    return render_template("home.html", message=message)


@views.route('/', methods=['POST', 'GET'])
def reservations():
    pass


@views.route('/', methods=['POST', 'GET'])
def create_reservation():
    pass


@views.route('/', methods=['POST', 'GET'])
def edit_reservation():
    pass


@views.route('/', methods=['POST', 'GET'])
def profile():
    pass