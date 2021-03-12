# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from . import cmdline


bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return render_template('login.html')
