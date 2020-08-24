# -*- coding: utf-8 -*-
import os

root_app = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def _make_dir(dir_name):
    """ Make log folder to store logs. """
    log_dir_path = os.path.join(root_app, dir_name)
    if not os.path.exists(log_dir_path):
        os.mkdir(log_dir_path)
    return log_dir_path


class BaseConfig(object):

    DEBUG = False
    TESTING = False

    ROOT_APP = root_app
    LOG_FOLDER = _make_dir('logs')
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(16).hex())


class Development(BaseConfig):

    DEBUG = True


class ProductionConfig(BaseConfig):

    DEBUG = False


class TestingConfig(BaseConfig):

    DEBUG = True
    TESTING = True
