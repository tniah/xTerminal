# -*- coding: utf-8 -*-
import os
import logging
import logging.handlers
from flask import Flask
from .extensions import socketio
from .core import bp as index_bp


def create_app(environment=None):
    app = Flask(__name__)

    __config_app(app=app, environment=environment)
    __init_extensions(app=app)
    __register_routes(app=app)
    return app


def __config_app(app, environment=None):
    environment = environment or app.config['ENV']
    if environment == 'production':
        app.config.from_object('app.config.ProductionConfig')
    elif environment == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.Development')
    return app


def __init_extensions(app):
    socketio.init_app(app=app)


def __register_routes(app):
    app.register_blueprint(blueprint=index_bp)


def __config_logging(app):
    """ Config logging for Flask application. """
    if app.config['ENV'] == 'production':
        fmt = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        formatter = logging.Formatter(fmt=fmt)
        info_log = os.path.join(app.config['LOG_FOLDER'], 'app-info.log')
        info_log_handler = logging.handlers.RotatingFileHandler(
            filename=info_log,
            maxBytes=1024**2,
            backupCount=10)
        info_log_handler.setLevel(level=logging.INFO)
        info_log_handler.setFormatter(fmt=formatter)
        app.logger.addHandler(info_log_handler)
    app.logger.setLevel(logging.INFO)
