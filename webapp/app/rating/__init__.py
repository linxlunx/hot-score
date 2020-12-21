from app import mongo
from flask import Blueprint, render_template, redirect, url_for, request
from app.rating.services import RatingService
from flask_login import login_required

rating = Blueprint('rating', __name__, url_prefix='/rating')


@rating.route('/')
@login_required
def index():
    r = RatingService()
    image = r.get_image()
    data = {
        '_id': str(image['_id']),
        'image': image['image'],
    }
    return render_template('rating/index.html', data=data)


@rating.route('/api/skip', methods=['POST'])
@login_required
def skip_image():
    if request.method == 'POST':
        _id = request.form.get('_id')
        if _id is None:
            return '0'

        r = RatingService()
        skipped = r.skip_image(_id)
        if not skipped:
            return '0'
        return '1'


@rating.route('/api/rate', methods=['POST'])
@login_required
def rate_image():
    if request.method == 'POST':
        _id = request.form.get('_id')
        rate = request.form.get('rate')
        if not all([_id, rate]):
            return '0'
        r = RatingService()
        rated = r.rate_image(_id, rate)
        if not rated:
            return '0'
        return '1'
