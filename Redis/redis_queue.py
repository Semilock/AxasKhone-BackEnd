import uuid
import json


class SimpleQueue(object):
    def __init__(self, conn, name):
        self.conn = conn
        self.name = name

    def enqueue(self, obj, *args):
        # task = SimpleTask(func, *args)
        # serialized_obj = json.dumps(obj)
        self.conn.lpush(self.name, obj)

    def dequeue(self):
        _, serialized_obj = self.conn.brpop(self.name)
        # obj = json.loads(serialized_obj)
        # task.process_task()
        return serialized_obj

    def get_length(self):
        return self.conn.llen(self.name)


class SimpleTask(object):
    def __init__(self, func, *args):
        self.id = str(uuid.uuid4())
        self.func = func
        self.args = args

    def process_task(self):
        self.func(*self.args)
