from flask import Flask

from app.configuration import APP_SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY

from app import service
from app import routes
