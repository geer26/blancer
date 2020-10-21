from flask import Flask
from config import Config, DevConfig, ProdConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

from app import routes