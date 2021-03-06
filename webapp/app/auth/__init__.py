from app import mongo, login
from flask_login import login_user, logout_user, current_user
from flask import request, redirect, render_template, flash, Blueprint, url_for
from app.auth.models import User
from app.auth.forms import LoginForm


auth = Blueprint('auth', __name__, url_prefix='/auth')
login.login_view = '/auth/login'


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        form = LoginForm()
        return render_template('auth/login.html', form=form)

    if request.method == 'POST':
        form = LoginForm(request.form)

        if not form.validate():
            flash('Please fill username/password')
            return redirect(url_for('auth.login'))

        user = mongo.db.users.find_one({'$and': [
            {'username': form.username.data},
            {'active': True}
        ]})

        if not user:
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        if User.check_password(user['password'], form.password.data):
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
