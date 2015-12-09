import tornado.httpserver
import tornado.ioloop
import tornado.web

from lib.imagize import Imagize

class ImagizeGenerator(tornado.web.RequestHandler):
    """
    Imagize Generator
    """
    imagizer = None
    filename = None

    def prepare(self):
        """
        prepare()
        """
        text_arg = self.get_argument('text', None)
        if text_arg is not None and len(text_arg) > 0:
            text_arg = str(text_arg.encode('utf-8'))

        self.imagizer = Imagize()
        self.filename = self.imagizer.generate(text_arg)

    def get(self):
        response, code = {'status': 'ok'}, 200
        self.set_header('Content-Type', 'text/html')
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        #self.set_status(code)
        self.write("<img src='http://54.152.150.121/v1/" + self.filename + "' />")
        #self.write(response)

    def post(self):

        response, code = {'status': 'ok'}, 200
        self.set_header('Content-Type', 'text/html')
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.set_status(code)
        self.filename = "http://54.152.150.121/v1/static/" + self.filename
        self.write("<a href='" + self.filename + "'>" + self.filename + "</a>")
        self.write(response)