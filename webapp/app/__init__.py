from flask import Flask, redirect, url_for
from flask_pymongo import PyMongo
from flask_script import Manager
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user

app = Flask(__name__, static_folder='static')

app.config.from_object('config')

# load mongo
mongo = PyMongo(app)

# load bcrypt
bcrypt = Bcrypt(app)

# load manager
manager = Manager(app)

login = LoginManager(app)


@app.route('/')
def main_index():
    return redirect(url_for('dashboard.index'))


@app.context_processor
def inject_user():
    if not current_user.is_authenticated:
        user = {}
    else:
        user = mongo.db.users.find_one({'username': current_user.username})
        if not user:
            user = {}
    return dict(my_user=user)


from app.auth import auth
from app.dashboard import dashboard
from app.users import users
from app.rating import rating


# register app
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(users)
app.register_blueprint(rating)
