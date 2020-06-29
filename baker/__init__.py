import os
import time
import glob
from datetime import datetime

from flask_cors import CORS
from flask import Flask, request, jsonify


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.from_object('config.py')

    os.makedirs(app.instance_path, exist_ok=True)

    from . import route
    app.register_blueprint(route.bp)

    from . import mysql
    mysql.init_app(app)

    return app
