from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import random

app = Flask(__name__)
app.secret_key = 'secret!'
socketio = SocketIO(app)

waiting_room = []  # List to hold waiting users
matches = {}  # Dictionary to hold matched users

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    gender = request.form['gender']
    seeking = request.form['seeking']
    session['gender'] = gender
    session['seeking'] = seeking
    return redirect(url_for('waiting'))

@app.route('/waiting')
def waiting():
    return render_template('waiting.html')

@socketio.on('join')
def handle_join(data):
    user = {
        'id': request.sid,
        'gender': session['gender'],
        'seeking': session['seeking'],
        'text': data['text']
    }
    waiting_room.append(user)
    session['user'] = user

    if len(waiting_room) > 1:
        match_users()

def match_users():
    if len(waiting_room) >= 2:
        user1 = waiting_room.pop(0)
        user2 = waiting_room.pop(0)
        room = str(random.randint(1000, 9999))
        matches[room] = (user1, user2)
        join_room(room, sid=user1['id'])
        join_room(room, sid=user2['id'])
        emit('match', {'room': room, 'partner_text': user2['text']}, room=user1['id'])
        emit('match', {'room': room, 'partner_text': user1['text']}, room=user2['id'])

@socketio.on('response')
def handle_response(data):
    room = data['room']
    response = data['response']
    user = session['user']

    if room in matches:
        user1, user2 = matches[room]
        partner = user1 if user['id'] == user2['id'] else user2
        if 'response' in partner:
            if partner['response'] == 'accept' and response == 'accept':
                emit('meetup', {'location': 'Coffee Shop'}, room=room)
            else:
                emit('rejected', room=room)
                leave_room(room, sid=user1['id'])
                leave_room(room, sid=user2['id'])
                del matches[room]
                waiting_room.append(user1)
                waiting_room.append(user2)
                match_users()
        else:
            user['response'] = response

if __name__ == '__main__':
    socketio.run(app)