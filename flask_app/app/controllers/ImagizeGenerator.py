from json.encoder import JSONEncoder
import socket
import os
import time
import calendar

import tornado.httpserver
import tornado.ioloop
import tornado.web

from lib.imagize import Imagize
from lib.db_wrapper import Database

class ImagizeGenerator(tornado.web.RequestHandler):
    """
    Imagize Generator
    """
    imagizer = None
    filename = None
    filepath = None
    webpath = None
    text_to_imagize = None
    user_uuid = None
    app_uuid = None
    timestamp = None
    enc_text = None
    response = {}

    def prepare(self):
        """
        prepare()
        """
        self.text_to_imagize = self.get_argument('text', None)
        self.user_uuid = self.get_argument('user_uuid', None)
        self.app_uuid = self.get_argument('app_uuid', None)
        self.timestamp = int(self.get_argument('timestamp', None))

        self.set_header('Content-Type', 'application/json')
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')

        if not self.text_to_imagize or not self.user_uuid or not self.app_uuid or not self.timestamp:
            self.exit("Missing required parameters")

        if self.text_to_imagize is not None and len(self.text_to_imagize) > 0:
            self.text_to_imagize = str(self.text_to_imagize.encode('utf-8'))

        self.imagizer = Imagize()
        self.response = self.imagizer.prep(self.text_to_imagize, self.user_uuid, self.app_uuid)

        # We didn't have anything cached...send it back
        if self.response is None:
            self.filename, self.filepath, self.webpath, self.enc_text = self.imagizer.generate()
            self.response = { '_id': self.enc_text,
                         'status': 'ok',
                         'local_path': os.path.join(self.filepath, self.filename),
                         'web_path': self.webpath,
                         'file_name': self.filename,
                         'host_name': socket.gethostname(),
                         'user_uuid': self.user_uuid,
                         'app_uuid': self.app_uuid,
                         'rx_timestamp': self.timestamp,
                         'tx_timestamp': calendar.timegm(time.gmtime()),
                         'runtime': calendar.timegm(time.gmtime()) - self.timestamp,
                         'bucket': "" }
            db = Database(None) # fetch a singleton
            db.collection.insert(self.response)

    def exit(self, msg=None, code=403):
        response = {'id': 'PERM_DENIED', 'msg': msg}
        self.set_status(code)
        self.write(JSONEncoder().encode(response))
        self.finish()

    def post(self, code=200):
        self.set_status(code)
        self.write(self.response)
        self.finish()

    def get(self, code=200):
        self.set_status(code)
        self.write(self.response)
        self.finish()