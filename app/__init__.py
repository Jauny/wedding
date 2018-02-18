from flask import Flask, render_template

import logging
# setup logging https://docs.python.org/2/howto/logging.html#a-simple-example

app = Flask(__name__)

app.config.from_pyfile('config.cfg')
config = app.config
logger = app.logger

from app import views