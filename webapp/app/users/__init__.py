from app import bcrypt
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.users.services import UserService
from app.users.forms import UserEditRegistrationForm



users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/')
@login_required
def index():
    u = UserService()
    return render_template('users/index.html', users=u.user_list())


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
            form = UserEditRegistrationForm(email=user['email'], role=user['role'], status=status)
        else:
            form = UserEditRegistrationForm(email=user['email'])
        return render_template('users/edit.html', user=user, form=form)
    if request.method == 'POST':
        form = UserEditRegistrationForm(request.form)
        if form.validate():
            if form.password.data:
                if not form.password.data:
                    return render_template('users/edit.html', user=user, form=form)

                if form.password.data != form.confirm.data:
                    return render_template('users/edit.html', user=user, form=form)

            u = UserService()
            if u.check_email(form.email.data, user):
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
