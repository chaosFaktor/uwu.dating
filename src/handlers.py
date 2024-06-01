import tornado
import torndsession
from .services import TemplatingEngine

from .services.config import ConfigLoader

from .services.SessionManager import SessionManager

cfg = ConfigLoader(enable_sections=[])
#cfg_server = cfg.get('server')

class StartpageHandler(torndsession.sessionhandler.SessionBaseHandler):
    def get(self):
        session_manager = SessionManager(self.session)
        session_manager.reset_session()
        
        print(session_manager.get_session()["user"]["id"])
        self.write(session_manager.get_session()["user"]["id"])
        #self.write(TemplatingEngine.render("assets/sites/startpage.json"))
    
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