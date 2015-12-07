import tornado.httpserver
import tornado.ioloop
import tornado.web

class LoadBalancerHandler(tornado.web.RequestHandler):
    """
    Load Balancer Handler
    Handles /f5
    """

    def get(self):
        """
        get()
        """
        response, code = {'status': 'ok'}, 200
        self.set_header('Content-Type', 'text/plain')
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.set_status(code)
        self.write(response)