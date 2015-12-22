"""
JSONEncoder
"""
from __future__ import division
import json
from datetime import datetime
from bson.objectid import ObjectId

class JSONEncoder(json.JSONEncoder):
    """
    JSONEncoder
    """
    def default(self, our_object):
        """
        default()
        @params - self [Python Ref]
        Converts Object Id's to strings in JSON
        :param our_object:
        """
        if isinstance(our_object, ObjectId):
            return str(our_object)
        elif isinstance(our_object, datetime):
            return our_object.isoformat()

        return json.JSONEncoder.default(self, our_object)

    @staticmethod
    def encode_float_repr(value, precision):
        """
        encode_float_repr()
        Encode value with specified float precision
        :param precision:
        :param value:
        """
        if precision is not None:
            zerofill = 0
            zerofill_divisor = 1
            if precision[:1] == '-':
                zerofill = int(precision[1:])
                zerofill_divisor = 10 ** zerofill
                precision = '0'
            original_float_repr = json.encoder.FLOAT_REPR
            json.encoder.FLOAT_REPR = lambda o: format(o / zerofill_divisor if len(str(int(o))) > zerofill else o, '0<' + str(len(str(int(o)))) + '.' + str(precision) + 'f')

        encoded = json.JSONEncoder().encode(value)

        if precision is not None:
            json.encoder.FLOAT_REPR = original_float_repr

        return encoded

    @staticmethod
    def decode_list(data):
        rv = []
        for item in data:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = JSONEncoder.decode_list(item)
            elif isinstance(item, dict):
                item = JSONEncoder.decode_dict(item)
            rv.append(item)
        return rv
    
    @staticmethod
    def decode_dict(data):
        rv = {}
        for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = JSONEncoder.decode_list(value)
            elif isinstance(value, dict):
                value = JSONEncoder.decode_dict(value)
            rv[key] = value
        return rv