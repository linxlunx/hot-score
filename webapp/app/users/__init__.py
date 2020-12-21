from app import bcrypt
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.users.services import UserService
from app.users.forms import UserEditForm, UserAddForm


users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/')
@login_required
def index():
    u = UserService()
    return render_template('users/index.html', users=u.user_list())


@users.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    u = UserService()
    if u.role != 'admin':
        return redirect(url_for('users.index'))
    if request.method == 'GET':
        form = UserAddForm()
        return render_template('users/add.html', form=form)
    if request.method == 'POST':
        form = UserAddForm(request.form)

        if not form.validate():
            return render_template('users/add.html', form=form)

        if u.user_get(form.username.data):
            form.username.errors.append("Please use another username")
            return render_template('users/add.html', form=form)

        if u.email_is_exist(form.email.data):
            form.email.errors.append("Please use another email")
            return render_template('users/add.html', form=form)

        u.user_store({
            'username': form.username.data,
            'email': form.email.data,
            'password': bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
            'role': form.role.data,
            'active': True if form.status.data == 'active' else False,
        })

        return redirect(url_for('users.index'))


@users.route('/edit/<username>', methods=['GET', 'POST'])
@login_required
def edit(username):
    u = UserService()
    user = u.user_get(username)
    if not user:
        return redirect(url_for('users.index'))
    if request.method == 'GET':
        if u.role == 'admin':
            if user['role']:
                status = 'active'
            else:
                status = 'inactive'
            form = UserEditForm(email=user['email'], role=user['role'], status=status)
        else:
            form = UserEditForm(email=user['email'])
        return render_template('users/edit.html', user=user, form=form)
    if request.method == 'POST':
        form = UserEditForm(request.form)
        if form.validate():
            if form.password.data:
                if not form.password.data:
                    return render_template('users/edit.html', user=user, form=form)

                if form.password.data != form.confirm.data:
                    return render_template('users/edit.html', user=user, form=form)

            u = UserService()
            if u.check_email_change(form.email.data, user):
                form.email.errors.append("Please use another email!")
                return render_template('users/edit.html', user=user, form=form)

            if u.role == 'admin':
                update = {
                    'email': form.email.data,
                    'role': form.role.data,
                    'active': True if form.status.data == 'active' else False,
                }
            else:
                update = {
                    'email': form.email.data
                }

            if form.password.data:
                update['password'] = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            updated = u.user_update(username, update)
            return redirect(url_for('users.index'))
        else:
            return render_template('users/edit.html', user=user, form=form)
