from flask import Blueprint, render_template
from flask_login import current_user

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
def index():
    print(current_user.username)
    return render_template('dashboard/index.html')
