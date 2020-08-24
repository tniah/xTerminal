# -*- coding: utf-8 -*-
from flask_socketio import emit
from ..extensions import socketio


@socketio.on('cmdline', namespace='/cmdline')
def run_cmd(cmdline):
    print(cmdline)
    emit('cmdline', 'Hello baby!!!')
