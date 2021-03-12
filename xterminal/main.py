# Copyright 2021 by TNiaH <kainguyen1509@gmail.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Entry point for the application."""
import os

from flask import Flask

import config
from xterminal.extensions import g_auth
from xterminal.views.home import home_view
from xterminal.views.login import login_view


def create_app(config_file=None):
    """Create the Flask app instance.

    Returns:
        Application object (instance of flask.Flask)
    """
    app = Flask(__name__)
    # Load default settings
    app.config.from_pyfile(config.DEFAULT_SETTINGS)

    # Load settings from environment variable
    if 'xTERMINAL_SETTINGS' in os.environ:
        app.config.from_pyfile(os.environ['xTERMINAL_SETTINGS'])

    if config_file:
        app.config.from_pyfile(config_file)

    # Configure Flask logger
    configure_logger(app)

    # Initialize Flask extensions
    g_auth.init_app(app)

    # Register blueprints
    app.register_blueprint(login_view)
    app.register_blueprint(home_view)

    return app


def configure_logger(app):
    """Configure the logger.

    Args:
        app: The current Flask application
    """
    if app.debug:
        return

    import logging
    from logging.handlers import RotatingFileHandler

    # Set general log level
    app.logger.setLevel(logging.INFO)

    fmt = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    formatter = logging.Formatter(fmt)
    log_file = app.config.get('LOGFILE')
    log_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=1024 * 2,
        backupCount=10)
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(formatter)
