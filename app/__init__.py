from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from app.configuration import APP_SECRET_KEY, ENV, DB_URL

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
csrf = CSRFProtect(app)

from app import routes
from app.db.database import init_db
from app.service import start_expiration_services

init_db()
start_expiration_services()
