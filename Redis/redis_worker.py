import json
from urllib import request
import requests
import redis
import sys

sys.path.insert(1, "/home/kiana/akaskhoonemain/back/")

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
        data = obj_json.decode('utf-8')
        requests.post('http://127.0.0.1:8000/notifications/redis_actions/',
                      data=data,
                      headers={"Content-Type": "application/json"}
                      )


if __name__ == '__main__':
    worker()
