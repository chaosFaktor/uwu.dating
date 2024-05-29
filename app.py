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
    earnestness = request.form['earnestness']
    session['gender'] = gender
    session['earnestness'] = earnestness
    return redirect(url_for('earnestness'))

@app.route('/earnestness')
def earnestness():
    return render_template('earnestness.html')

@app.route('/earnest', methods=['POST'])
def earnest():
    real_earnestness = request.form['earnestness']
    session['real_earnestness'] = real_earnestness
    return redirect(url_for('questionnaire'))

@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')

@app.route('/questionnaire', methods=['POST'])
def questions():
    question1 = request.form['question1']
    question2 = request.form['question2']
    question3 = request.form['question3']
    question4 = request.form['question4']
    question5 = request.form['question5']
    session['question1'] = question1
    session['question2'] = question2
    session['question3'] = question3
    session['question4'] = question4
    session['question5'] = question5
    return redirect(url_for('waiting'))

@app.route('/waiting')
def waiting():
    return render_template('waiting.html')

@socketio.on('join')
def handle_join(data):
    user = {
        'id': request.sid,
        'gender': session['gender'],
        'earnestness': session['earnestness'],
        'real_earnestness': session['real_earnestness'],
        'question1': session['question1'],
        'question2': session['question2'],
        'question3': session['question3'],
        'question4': session['question4'],
        'question5': session['question5'],
    }
    waiting_room.append(user)
    session['user'] = user

    if len(waiting_room) > 1:
        match_users()

def match_users():
    if len(waiting_room) > 1:
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