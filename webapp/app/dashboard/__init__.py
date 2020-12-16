from flask import Blueprint, render_template
from flask_login import current_user, login_required

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
@login_required
def index():
    return render_template('dashboard/index.html', data={
        'username': current_user.username
    })
