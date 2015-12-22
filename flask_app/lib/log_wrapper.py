"""
LogWrapper
"""
import logging
import os
import datetime
import time

from singleton import Singleton


loggers = { }


class LogWrapper:
    """
    LogWrapper
    This class grants us an abstraction layer ontop of Python's default logging library.
    """
    __metaclass__ = Singleton
    logger = None
    class_settings = None

    def __init__(self, config=None):
        """
        Constructor
        @param - self [python reference]
        @param - config [Dictionary|None]
        @return - None
        """
        self.class_settings = config if config else None
        app_name = self.class_settings['application']
        file_name = app_name
        # Inject the process and log name in order to allow non-blocking per-process writes
        if 'port' in self.class_settings and self.class_settings['port']:
            file_name = app_name + "_" + str(self.class_settings['port'])

        now = datetime.datetime.utcnow()
        file_name = "%s_%d_%d_%d" % (file_name, now.month, now.day, now.year)
        logging.Formatter.converter = time.gmtime
        self.logger = logging.getLogger(file_name)
        self.logger.setLevel(self.class_settings['logLevel'])
        file_path = os.path.join(self.class_settings['logDir'], file_name + '.log')

        # default :: maxBytes=25MB || backupCount=25 || max log space = ~655MB
        max_bytes = 26214400  # 25MB*1024*1024
        backup_count = 25

        # config based override of defaults
        if 'logging' in config:
            if 'max_bytes' in config['logging']:
                max_bytes = config['logging']['max_bytes']
            if 'backup_count' in config['logging']:
                backup_count = config['logging']['backup_count']

        handler = logging.handlers.RotatingFileHandler(file_path, maxBytes=max_bytes, backupCount=backup_count)
        formatter = logging.Formatter(
            '[%(asctime)s] PID=%(process)s {%(pathname)s:%(lineno)d} %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def flatten(self, data, path=''):
        """
        flatten
        @return - flat_list [list]
        :param data:
        :param path:
        """
        flat_list = []
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    flat_list.extend(self.flatten(v, str(path) + str(k.upper()) + '_'))
                elif isinstance(v, list):
                    count = 0
                    for item in v:
                        item_path = path + k.upper() + '_' + str(count) + '_'
                        flat_list.extend(self.flatten(item, str(item_path)))
                        count += 1
                else:
                    if isinstance(v, unicode):
                        v = v.encode('utf-8')
                    flat_list.append('%s%s=%s' % (str(path), str(k.upper()), str(v)))
        elif isinstance(data, str):
            flat_list.append('%s=%s' % (str(path), str(data)))
        return flat_list

    def get_log(self, msg=None, data=None):
        """
        get_log
        @return - log [string]
        :param data:
        :param msg:
        """
        valid_data = isinstance(data, dict)
        log = ''
        if msg:
            log = msg
            if data and valid_data:
                log += ' '
        if data and valid_data:
            log += ', '.join(self.flatten(data))
        return log.decode('utf-8')

    def myLogger(self):
        return self.logger