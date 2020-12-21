from app import mongo
from flask import Blueprint, render_template, redirect, url_for, request
from app.rating.services import RatingService
from flask_login import login_required

rating = Blueprint('rating', __name__, url_prefix='/rating')


@rating.route('/')
@login_required
def index():
    return render_template('rating/index.html')
