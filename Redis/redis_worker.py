import json
from urllib import request
import requests
import redis
import sys


sys.path.insert(1, "/home/arghavan/rahnema/back/")

from Redis.redis_queue import SimpleQueue
from os import environ
environ.setdefault('DJANGO_SETTINGS_MODULE', "settings")
import django

django.setup()


def worker():
    r = redis.Redis()
    queue = SimpleQueue(r, 'queue')
    while True:
        print("Dequeue-ing")
        obj_json = queue.dequeue()
        print(obj_json)
        obj_json = obj_json.decode('utf-8')
        # print(obj_json, type(obj_json))
        # data= data.replace("\'","\"")
        # data = data.replace("F", "f")
        # data = data.replace("T", "t")
        # print(data)
        # data = json.loads(data)
        # print(data)
        requests.post('http://127.0.0.1:8000/notifications/save_to_database/',
                      data=obj_json
                      , headers={"Content-Type":"application/json"})
                      # )

if __name__ == '__main__':
    worker()
