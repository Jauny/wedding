import logging
from flask import Flask

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)

app.config.from_pyfile('config.cfg')
config = app.config

from app import views
