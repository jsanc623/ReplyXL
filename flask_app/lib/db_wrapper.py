from pymongo import MongoClient
from lib.singleton import Singleton

class Database(object):
    __metaclass__ = Singleton

    config = None
    host = None
    port = 27017
    max_pool_size = 100
    is_replica_set = False
    w = 0
    replicaSet = None

    client = None
    database = None
    collection = None

    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        if self.is_replica_set:
            self.client = MongoClient(self.host, self.port, connect=True, maxPoolSize=self.max_pool_size,
                                      w=self.w, replicaSet=self.replicaSet, readPreference=SECONDARY_PREFERRED)
        else:
            self.client = MongoClient(self.host, self.port, connect=True, maxPoolSize=self.max_pool_size)

        self.database = self.client[self.config['mongo']['database']]
        self.collection = self.database[self.config['mongo']['collection']]

    def collection_instance(self):
        return self.collection