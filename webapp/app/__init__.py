from flask import Flask, redirect, request, render_template, flash
from flask_pymongo import PyMongo
from flask_script import Manager
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user

from app.dashboard import dashboard

app = Flask(__name__, static_folder='static')

app.config.from_object('config')

# load mongo
mongo = PyMongo(app)

# load bcrypt
bcrypt = Bcrypt(app)

# load manager
manager = Manager(app)

login = LoginManager(app)
login.login_view = 'login'


# login manager
class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return bcrypt.check_password_hash(password_hash, password)

    @login.user_loader
    def load_user(username):
        u = mongo.db.users.find_one({'username': username})
        if not u:
            return None
        return User(username=u['username'])

    @app.route('/auth/login', methods=['GET', 'POST'])
    def auth_login():
        if request.method == 'GET':
            if current_user.is_authenticated:
                return redirect('/dashbboard')
            return render_template('auth/login.html')

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if not all([username, password]):
                return redirect('/auth/login')

            user = mongo.db.users.find_one({'$and': [
                {'username': username},
                {'active': True}
            ]})

            if not user:
                flash('Invalid username or password')
                return redirect('/auth/login')

            if User.check_password(user['password'], password):
                user_obj = User(username=user['username'])
                login_user(user_obj)
                return redirect('/dashboard')
            else:
                flash('Invalid username or password')
                return redirect('/auth/login')

    @app.route('/auth/logout')
    def logout():
        logout_user()
        return redirect('/auth/login')


# register app
app.register_blueprint(dashboard)
