from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join_room')
def on_join_room(data):
    room = data['room']
    join_room(room)
    emit('user_joined', f'{request.sid} has joined the room {room}.', room=room)

@socketio.on('leave_room')
def on_leave_room(data):
    room = data['room']
    leave_room(room)
    emit('user_left', f'{request.sid} has left the room {room}.', room=room)

@socketio.on('send_message_to_room')
def handle_send_message_to_room(data):
    room = data['room']
    message = data['message']
    emit('room_message', message, room=room)

if __name__ == '__main__':
    socketio.run(app)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Example</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <input type="text" id="room" placeholder="Type room name">
    <button id="join">Join Room</button>
    <button id="leave">Leave Room</button>
    <br>
    <input type="text" id="message" placeholder="Type your message">
    <button id="send">Send to Room</button>
    <ul id="messages"></ul>

    <script>
        const socket = io();
        $('#join').click(() => {
            const room = $('#room').val();
            socket.emit('join_room', { room });
        });

        $('#leave').click(() => {
            const room = $('#room').val();
            socket.emit('leave_room', { room });
        });

        $('#send').click(() => {
            const room = $('#room').val();
            const message = $('#message').val();
            socket.emit('send_message_to_room', { room, message });
            $('#message').val('');
        });

        socket.on('user_joined', (msg) => {
            $('#messages').append($('<li>').text(msg));
        });

        socket.on('user_left', (msg) => {
            $('#messages').append($('<li>').text(msg));
        });

        socket.on('room_message', (message) => {
            $('#messages').append($('<li>').text(message));
        });
    </script>
</body>
</html>
