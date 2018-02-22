import os
import logging
from flask import Flask

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)

app.config.from_pyfile('config.cfg')
config = app.config
app.secret_key = os.environ.get('SECRET_KEY')

from app import views  # noqa
