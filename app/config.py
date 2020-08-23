# -*- coding: utf-8 -*-
import os


class BaseConfig(object):

    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(16).hex())


class Development(BaseConfig):

    DEBUG = True


class ProductionConfig(BaseConfig):

    DEBUG = False


class TestingConfig(BaseConfig):

    DEBUG = True
    TESTING = True
