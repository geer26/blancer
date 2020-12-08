from flask import Flask
from config import SQLite, PostgreSQL
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO

app = Flask(__name__)
#app.config.from_object(SQLite)
app.config.from_object(PostgreSQL)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

socket = SocketIO(app)
socket.init_app(app, cors_allowed_origins="*")

migrate = Migrate(app, db, render_as_batch=True)

login = LoginManager(app)

from app import routes,models