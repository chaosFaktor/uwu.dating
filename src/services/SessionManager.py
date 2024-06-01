import secrets


from .config import ConfigLoader


class SessionManager:
    def __init__(self, session):
        cfg = ConfigLoader(enable_sections=["session"])
        self.cfg_session = cfg.get('session')

        self.session = session
        self.session_template = {
            "user": {
                "id": None,
                "data": {
                    'gender': None,
                    'earnestness': None,
                    'real_earnestness': None,
                    'cat_ears': None,
                    'cat_ear_color': None,
                    'dect': None,
                    'distinguish': None
                },
                "logged_in": False
            }
        }
    def register_user_session(self):
        if ("user" in self.session):
            return self
        else:
            self.session["user"] = self.session_template
            self.session["user"]["id"] = secrets.token_urlsafe(self.cfg_session["session-id-secret-length"])
        return self
    def set_user_data(self, gender, earnestness, real_earnestness, cat_ears, distinguish, cat_ear_color=None, dect=None):
        self.session["user"]["data"] = {
            "gender": gender,
            "earnestness": earnestness,
            'real_earnestness': None,
            'cat_ears': None,
            'cat_ear_color': None,
            'dect': None,
            'distinguish': None
            
        }
        return self
        
    def get_session(self):
        return self.session