from flask import Flask
from app.dashboard import dashboard
from app.auth import auth

app = Flask(__name__, static_folder='static')

app.config.from_object('config')

# register app
app.register_blueprint(dashboard)
app.register_blueprint(auth)
