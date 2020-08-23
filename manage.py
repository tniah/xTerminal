# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['SECRET_KEY'] = 'my_secret'
app.config['DEBUG'] = True
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('message')
def handle_message(message):
    print('received message: ' + str(message))


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
