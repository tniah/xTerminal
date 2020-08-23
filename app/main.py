# -*- coding: utf-8 -*-
from flask import Flask, render_template
from .extensions import socketio


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

    @app.route('/')
    def index():
        return render_template('index.html')
