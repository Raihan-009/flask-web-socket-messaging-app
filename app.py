from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', f'{username} has joined the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('message', f'{username} has left the room.', room=room)

@socketio.on('client_message')
def handle_client_message(data):
    room = data['room']
    message = data['message']
    emit('client_message', {'username': data['username'], 'message': message}, room=room)

if __name__ == '__main__':
    socketio.run(app)
