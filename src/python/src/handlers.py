import tornado
import torndsession
import asyncio
import json

from .services import TemplatingEngine

from .services.config import ConfigLoader


from .services.User import User, UserManager


cfg = ConfigLoader(enable_sections=[])
#cfg_server = cfg.get('server')


class StartpageHandler(torndsession.sessionhandler.SessionBaseHandler):
    def get(self):
        if (self.session.get("id") == None):
            self.session["id"] = UserManager.register_new_user(User())
        session_id = self.session["id"]
        user = User()
        UserManager.set_user(user, session_id)
        user = UserManager.get_user_by_session_id(session_id)
        if (user.get_loggedin()):
            print("user is logged in")
            self.redirect("/app/waiting_room")
        else:
            print("user is not logged in")
            self.redirect("/login")

class LoginHandler(torndsession.sessionhandler.SessionBaseHandler):
    def get(self):
        if (self.session.get("id") == None):
            self.session["id"] = UserManager.register_new_user(User())
        self.write(TemplatingEngine.render("assets/sites/login.json"))

class LoginDoHandler(torndsession.sessionhandler.SessionBaseHandler):
    def post(self):
        session_id = self.session.get('id')
        if (session_id == None):
            session_id = UserManager.register_new_user(User())
            self.session['id'] = session_id
        user = UserManager.get_user_by_session_id(session_id)
        data = json.loads(self.request.body.decode('utf-8'))
        user.set_user_data(
            gender=data.get("gender"),
            earnestness=data.get("earnestness"),
            cat_ears=data.get("cat_ears"),
            cat_ear_color=data.get("color"),
            dect=data.get("dect"),
            distinguish=data.get("distinguish")
        )
        user.set_logged_in(True)
        self.redirect("/app/waiting_room")
        
class PrivateChatHandler(torndsession.sessionhandler.SessionBaseHandler):
    def get(self):
        session_id = self.session.get('id')
        if (session_id == None):
            self.redirect("/login")
            return
        user = UserManager.get_user_by_session_id(session_id)
        if (user.get_match() == None):
            self.redirect("/")
            return
        user.set_status(User.Status.IN_CHAT)
        match = user.get_match() 
        bonus_data = {
            "user_info": match.get_public_data()
        }
        bonus_data['user_info']['meetup_location'] = user.get_meetup_location()
        print(bonus_data)
        print(user.get_public_data())
        print(match.get_public_data())
        print("-----")
        self.write(TemplatingEngine.render("assets/sites/private_chat.json", bonus_data=bonus_data))

class WaitingRoomHandler(torndsession.sessionhandler.SessionBaseHandler):
    def get(self):
        if (self.session.get("id") == None):
            self.session["id"] = UserManager.register_new_user(User())
        user = UserManager.get_user_by_session_id(self.session.get("id"))
        if (not user.get_loggedin()):
            self.redirect("/login")
            return
        self.write(TemplatingEngine.render("assets/sites/waiting_room.json"))
        
class WebSocketHandler(tornado.websocket.WebSocketHandler, torndsession.sessionhandler.SessionBaseHandler):
    def open(self):
        print("WebSocket opened")
        self.user = UserManager.get_user_by_session_id(self.session["id"])
        self.user.set_ws_handler(self)
        
    def on_message(self, text):
        if (self.session.get("id") == None):
            return
        session_id = self.session["id"]
        sender = UserManager.get_user_by_session_id(session_id)
        if (not sender.get_loggedin()):
            return
        msg = json.loads(text)
        if (msg["type"] == "match/register"):
            UserManager.MatchMaking.register(self.user)
            self.user.set_status(User.Status.IN_WAITING_ROOM)
        elif (msg["type"] == "chat/connect"):
            sender = UserManager.get_user_by_session_id(session_id)
            sender.set_status(User.Status.IN_CHAT)

            receivant = sender.get_match()
            if (receivant.get_status() == User.Status.IN_CHAT):
                sender.send_ws_msg(json.dumps({
                    "type": "chat/connect",
                    "success": True
                }))
            else:
                sender.send_ws_msg(json.dumps({
                    "type": "chat/connect",
                    "success": False
                }))
        elif (msg["type"] == "chat/message"):
            sender = UserManager.get_user_by_session_id(session_id)

            receivant = sender.get_match()
            if (msg.get("text") == None):
                return
            if (receivant.get_status() == User.Status.IN_CHAT):
                receivant.send_ws_msg(json.dumps({
                    "type": "chat/message",
                    "text": msg.get("text")
                }))


    def on_close(self):
        if (self.user.get_match() == None):
            return
        self.user.get_match().send_ws_msg(json.dumps({
            "type": "chat/disconnect"
        }))
        self.user.set_status(User.Status.INACTIVE)
        print("WebSocket closed")
    
class CssHandler(tornado.web.StaticFileHandler):
    @classmethod
    def set_extra_header(self, path):
        self.set_header('Content-Type','text/css')  
class JsHandler(tornado.web.StaticFileHandler):
    @classmethod
    def set_extra_header(self, path):
        self.set_header('Content-Type', 'text/javascript')
class FontHandler(tornado.web.StaticFileHandler):
    @classmethod
    def set_extra_header(self, path):
        pass