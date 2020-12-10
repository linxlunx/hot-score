from flask import Flask
from app.dashboard import dashboard

app = Flask(__name__, static_folder='static')

app.config.from_object('config')

# register app
app.register_blueprint(dashboard)
