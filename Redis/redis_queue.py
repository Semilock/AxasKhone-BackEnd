import uuid
import json


class SimpleQueue(object):
    def __init__(self, conn, name):
        self.conn = conn
        self.name = name

    def enqueue(self, obj, *args):
        self.conn.lpush(self.name, obj)

    def dequeue(self):
        _, serialized_obj = self.conn.brpop(self.name)
        return serialized_obj

    def get_length(self):
        return self.conn.llen(self.name)
