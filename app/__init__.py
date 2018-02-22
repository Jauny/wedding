import os
import logging

from flask import Flask


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)

from app.config import ConfigDev, ConfigProd  # noqa
if os.environ.get('ENVIRONMENT') is 'PRODUCTION':
    config = ConfigProd()
else:
    config = ConfigDev()
app.config.from_mapping(config)
app.secret_key = app.config.get('SECRET_KEY')

from app import views  # noqa
