from flask import Flask, redirect, url_for
from flask_pymongo import PyMongo
from flask_script import Manager
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

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


from app.auth import auth
from app.dashboard import dashboard

# register app
app.register_blueprint(auth)
app.register_blueprint(dashboard)
