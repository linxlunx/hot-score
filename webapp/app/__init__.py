from flask import Flask
from flask_pymongo import PyMongo
from flask_script import Manager
from flask_bcrypt import Bcrypt

from app.dashboard import dashboard
from app.auth import auth

app = Flask(__name__, static_folder='static')

app.config.from_object('config')

# load mongo
mongo = PyMongo(app)

# load bcrypt
bcrypt = Bcrypt(app)

# load manager
manager = Manager(app)


# register app
app.register_blueprint(dashboard)
app.register_blueprint(auth)
