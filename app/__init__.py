from flask import Flask
from config import Config, DevConfig, ProdConfig
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
#from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(DevConfig)
#app.config.from_object(ProdConfig)
#change at deployment!

print(app.config['SENDGRID_API_KEY'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

socket = SocketIO(app)
socket.init_app(app, cors_allowed_origins="*")
#enable at deployment!

#mail = Mail(app)

migrate = Migrate(app, db, render_as_batch=True)

login = LoginManager(app)

from app import routes,models