from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app import mongo
import hashlib
from app.rating.services import RatingService


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
@login_required
def index():
    r = RatingService()
    total = r.get_total()
    rated = r.get_total({'is_labeled': True})
    skipped = r.get_total({'is_skipped': True})
    return render_template('dashboard/index.html', total=total, rated=rated, skipped=skipped)
