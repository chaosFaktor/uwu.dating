import asyncio
import tornado
from tornado import websocket
from torndsession import sessionhandler
from .services.config import ConfigLoader

from .services.User import User, UserManager

from .handlers import *

cfg = ConfigLoader(enable_sections=['server', 'session'])
cfg_server = cfg.get('server')
cfg_session = cfg.get('session')

class App(tornado.web.Application):

    def __init__(self):
        settings = {
        }
        session_settings = {
            "driver": 'memory',
            "driver_settings": {'host': self},
            "force_persistence": True,
            "sid_name": 'torndsessionID',
            "session_lifetime": cfg_session['lifetime']
        }
        settings.update(session=session_settings)

        self.app = tornado.web.Application([
            (r"/", StartpageHandler),
            (r"/login", LoginHandler),
            (r"/login_do", LoginDoHandler),
            (r"/app/waiting_room", WaitingRoomHandler),
            (r"/app/chat", PrivateChatHandler),
            (r"/css/(.*)", CssHandler, {"path": "./css"}),
            (r"/js/(.*)", JsHandler, {"path": "./js"}),
            (r"/static/fonts/(.*)", FontHandler, {"path": "./assets/fonts"}),
            (r"/ws", WebSocketHandler)
        ], **settings)



    async def main(self):
        self.app.listen(cfg_server['port'])
        while True:
            try:
                for (i,o, location) in UserManager.MatchMaking.get_matches():
                    try:
                        i.get_match().set_match(None)
                    except:
                        pass
                    i.set_match(o)
                    i.set_meetup_location(location)
                    i.send_ws_msg(json.dumps({
                        "type": "match/found",
                        "id": o.get_session_id()
                    }))
                    try:
                        o.get_match().set_match(None)
                    except:
                        pass
                    o.set_match(i)
                    o.set_meetup_location(location)
                    o.send_ws_msg(json.dumps({
                        "type": "match/found",
                        "id": i.get_session_id()
                    }))
            except Exception as e:
                print(str(e))
                open("logs/err/mainloop", "a").write(str(e)+"\n")
                        
            await asyncio.sleep(0.7)

    def run(self):
        asyncio.run(self.main())
