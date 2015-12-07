from json.encoder import JSONEncoder

import tornado.httpserver
import tornado.ioloop
import tornado.web

class StatusHandler(tornado.web.RequestHandler):
    """
    Status Handler
    Handles /statuscheck
    """

    def prepare(self):
        """
        get()
        """
        response, code = None, None
        self.set_header('Content-Type', 'application/json')
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.set_status(code)
        self.write(JSONEncoder().encode(response))

    def get(self):
        pass

    def post(self):
        pass

class MissingHandler(tornado.web.RequestHandler):
    """
    Missing Handler
    Handles /404
    """

    def prepare(self):
        """
        get()
        """
        code = 404
        response = {'id': 'NOT_FOUND'}
        self.set_header('Content-Type', 'application/json')
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.set_status(code)
        self.write(JSONEncoder().encode(response))

    def get(self):
        pass

    def post(self):
        pass

class DenyHandler(tornado.web.RequestHandler):
    """
    DenyHandler
    """

    def prepare(self):
        """
        Deny connection with 403 PERM_DENIED error
        """
        code = 403
        response = {'id': 'PERM_DENIED'}
        self.set_header('Content-Type', 'application/json')
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.set_status(code)
        self.write(JSONEncoder().encode(response))

    def get(self):
        pass

    def post(self):
        pass