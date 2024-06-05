from tornado import websocket

import secrets

from .config import ConfigLoader


cfg = ConfigLoader(enable_sections=['session', 'match_making'])
cfg_match_making = cfg.get('match_making')
cfg_session = cfg.get('session')

class UserManager:
    sessions = {}
    @classmethod
    def get_all_sessions(self):
        return self.sessions
    @classmethod
    def get_user_by_session_id(self, session_id):
        return self.sessions[session_id]
    @classmethod
    def set_user(self, user, session_id):
        user.set_session_id(session_id)
        if(self.sessions.get(session_id) != None):
            return False
        self.sessions[session_id] = user
    @classmethod
    def register_new_user(self, user):
        session_id = secrets.token_urlsafe(cfg_session['session-id-length'])
        user.set_session_id(session_id)
        self.set_user(user, session_id)
        return session_id
        
    class MatchMaking:
        meetup_locations = cfg_match_making["meetup_locations"]
        queue = []
        @classmethod
        def register(self, user):
            if (not user in self.queue):
                self.queue.append(user)                        
        @classmethod
        def get_single_match(self):
            if (len(self.queue) <= 2):
                return
            pair = (self.queue[0], self.queue[1])
            self.queue = self.queue[2:]
            return pair
        @classmethod
        def get_matches(self):
            while True:
                if (len(self.queue) < 2):
                    return
                pair = (self.queue[0], self.queue[1], secrets.choice(self.meetup_locations))
                self.queue = self.queue[2:]
                yield pair

class User:
    def __init__(self,  status=None, logged_in=False, ws_handler = None, session_id = None):
        self.ws_handler = ws_handler
        self.status = status
        self.match = None
        self.session_id = None
        self.logged_in = logged_in
        self.meetup_location = None
        self.public_data = {
            'cat_ears': None,
            'dect': None,
            'distinguish': None
        }
        self.data = {
            'gender': None,
            'earnestness': None,
            'real_earnestness': None,
            'cat_ears': None,
            'cat_ear_color': None,
            'dect': None,
            'distinguish': None
        }
    def set_user_data(self, gender=None, earnestness=None, real_earnestness=None, cat_ears=None, distinguish=None, cat_ear_color=None, dect=None):
        self.data = {
            "gender": gender,
            "earnestness": earnestness,
            'real_earnestness': real_earnestness,
            'cat_ears': cat_ears,
            'cat_ear_color': cat_ear_color,
            'dect': dect,
            'distinguish': distinguish,
            
        }
        if (cat_ears != None):
            self.public_data["cat_ears"] = cat_ear_color
        if (dect != None):
            self.public_data["dect"] = dect
        if (distinguish != None):
            self.public_data["distinguish"] = distinguish

    def get_public_data(self):
        return self.public_data
    def set_ws_handler(self, ws_handler):
        self.ws_handler = ws_handler
    def set_logged_in(self, logged_in):
        self.logged_in = logged_in
    def set_session_id(self, session_id):
        self.session_id = session_id
    def get_session_id(self):
        return self.session_id
    def set_match(self, user):
        self.match = user
    def get_match(self):
        return self.match
    def set_status(self, status):
        self.status = status
    def get_status(self):
        return self.status
    def get_loggedin(self):
        return self.logged_in
    def set_meetup_location(self, location):
        self.meetup_location = location
    def get_meetup_location(self):
        return self.meetup_location

    def send_ws_msg(self, msg):
        try:
            self.ws_handler.write_message(msg)
            return True
        except websocket.WebSocketClosedError:
            return False

    class Status:
        INACTIVE = -1
        IN_WAITING_ROOM = 0
        IN_CHAT = 1
