from flask import Flask
from app.dashboard import dashboard

app = Flask(__name__)

# register app
app.register_blueprint(dashboard)
