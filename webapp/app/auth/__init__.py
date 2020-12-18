from app import mongo, login
from flask_login import login_user, logout_user, current_user
from flask import request, redirect, render_template, flash, Blueprint, url_for
from app.auth.models import User


auth = Blueprint('auth', __name__, url_prefix='/auth')
login.login_view = '/auth/login'


@auth.route('/login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return render_template('auth/login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username, password]):
            flash('Please fill username/password')
            return redirect(url_for('auth.login'))

        user = mongo.db.users.find_one({'$and': [
            {'username': username},
            {'active': True}
        ]})

        if not user:
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        if User.check_password(user['password'], password):
            user_obj = User(username=user['username'])
            login_user(user_obj)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/auth/login')
