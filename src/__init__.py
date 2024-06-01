import asyncio
import tornado
from torndsession import sessionhandler
from .services.config import ConfigLoader

from .handlers import *

cfg = ConfigLoader(enable_sections=['server'])
cfg_server = cfg.get('server')

class App(tornado.web.Application):

    def __init__(self):
        settings = {
        }
        session_settings = {
            "driver": 'memory',
            "driver_settings": {'host': self},
            "force_persistence": True,
            "sid_name": 'torndsessionID',
            "session_lifetime": 1800
        }
        settings.update(session=session_settings)

        self.app = tornado.web.Application([
            (r"/", StartpageHandler),
            (r"/static/css/(.*)", CssHandler, {"path": "./static/css"}),
            (r"/static/js/(.*)", JsHandler, {"path": "./static/js"}),
            (r"/static/fonts/(.*)", FontHandler, {"path": "./static/fonts"})
        ], **settings)



    async def main(self):
        self.app.listen(cfg_server['port'])
        await asyncio.Event().wait()

    def run(self):
        asyncio.run(self.main())
