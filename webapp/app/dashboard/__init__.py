from flask import Blueprint, render_template

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
def index():
    return render_template('dashboard/index.html')
