from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import random, time, json

app = Flask(__name__)
app.secret_key = 'secret!'
socketio = SocketIO(app)

TIMEOUT = 30

waiting_room = []  # List to hold waiting users
matches = {}  # Dictionary to hold matched users
last_check = time.time() # Implement periodic checks at some point
event_locations = ['the UwU-banner at the back side of the uv-tunnel',
'the game playing on the beamer in front of the uv-tunnel',
'the paws on the back side of the uv-tunnel',
'the rainbow laces vending machine near the Chaos Post',
'the electronics vending machine with niki fox sticks on top on the first floor',
'the multiplayer snake screen',
'the rope climbing location',
'the µPOC helpdesk at the eurobox-pile',
'the lamp in the UV-tunnel',
'the Chaos Post sign below the pride flag',
'the entrance of the lounge',
'the entrance to the ZKM-Kubus',
'the NOC-helpdesk and ask for Jesus',
'the boykisser-pride-flag on the bridge on the first floor above the bottle sorting station',
'the Lavawiese behind the kitchen tent',
'the entrance to the "(A)I Tell You, You Tell Me"-exhibition',
'the backside of the pride-flag on the second floor above the Chaos Post',
'the coin operated telephone at the µPOC',
'the sticker-desk near the entrance',
'the plants on the first floor above the troll desk']

waiting_room_joins = 0
match_offers = 0
meetups = 0

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
    if (request.form.get('earnestness')):
        real_earnestness = request.form['earnestness']
        session['real_earnestness'] = real_earnestness
    else:
        session['real_earnestness'] = None
    return redirect(url_for('recognition'))

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
    return redirect(url_for('recognition'))

@app.route('/recognition')
def recognition():
    return render_template('recognition.html')

@app.route('/recognition', methods=['POST'])
def recognition_form():
    cat_ears = request.form['cat_ears']
    session['cat_ears'] = cat_ears
    if cat_ears != '404':
        cat_ear_color = request.form['color']
        session['cat_ear_color'] = cat_ear_color
    else:
        session['cat_ear_color'] = None
    session['distinguish'] = request.form.get('distinguish')
    session['dect'] = request.form.get('dect')
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
        # 'question1': session['question1'],
        # 'question2': session['question2'],
        # 'question3': session['question3'],
        # 'question4': session['question4'],
        # 'question5': session['question5'],
        'cat_ears': session['cat_ears'],
        'cat_ear_color': session['cat_ear_color'],
        'dect': session['dect'],
        'distinguish': session['distinguish']
    }
    
    waiting_room.append(user)
    session['user'] = user

    waiting_room_joins += 1
    print('Match offers: ' + waiting_room_joins + '.')

    if len(waiting_room) > 1:
        match_users()

def match_users():
    if len(waiting_room) > 1:
        user1 = waiting_room.pop(0)
        user2 = waiting_room.pop(0)
        room = str(random.randint(1000, 9999999)) # avoid collision the easy way
        matches[room] = (user1, user2)
        join_room(room, sid=user1['id'])
        join_room(room, sid=user2['id'])
        user1_match_data = {i: user1[i] for i in user1 if i != 'id'}
        user2_match_data = {i: user2[i] for i in user2 if i != 'id'}
        emit('match', {'room': room, 'partner_data': json.dumps(user2_match_data), 'timeout': TIMEOUT}, room=user1['id'])
        emit('match', {'room': room, 'partner_data': json.dumps(user1_match_data), 'timeout': TIMEOUT}, room=user2['id'])
        match_offers += 1
        print('Match offers: ' + match_offers + '.')

@socketio.on('response')
def handle_response(data):
    room = data['room']
    response = data['response']
    user = session['user']

    if room in matches:
        if response == 'timeout':
            if 'response' in user:
                waiting_room.append(user)
                emit('return', room=room)
            else:
                emit('timeout', room=room)
            leave_room(room, sid=user['id'])
            del matches[room]
            return()

        user1, user2 = matches[room]
        partner = user1 if user['id'] == user2['id'] else user2

        if response == 'reject':
            emit('rejected', room=room)
            leave_room(room, sid=user1['id'])
            leave_room(room, sid=user2['id'])
            del matches[room]
            waiting_room.append(partner)
            waiting_room.append(user)
            return()

        if 'response' in partner:
            if partner['response'] == 'accept' and response == 'accept':
                location = get_location()
                emit('meetup', {'location': location}, room=room)
                meetups += 1
                print('Match offers: ' + meetups + '.')
        else:
            user['response'] = response

@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    emit('message', {'message': message, 'sender': session['user']['id']}, room=room)

def get_location():
    index = random.randint(0, len(event_locations) - 1)
    return event_locations[index]

if __name__ == '__main__':
    socketio.run(app)