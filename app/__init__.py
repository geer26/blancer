from flask import Flask
from config import Config, DevConfig, ProdConfig
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(DevConfig)

login = LoginManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes,models