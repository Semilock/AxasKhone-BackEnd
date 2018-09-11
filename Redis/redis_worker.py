from urllib import request
import requests
import redis
import sys


sys.path.insert(1, "/home/arghavan/rahnema/back/")

from Redis.redis_queue import SimpleQueue
from os import environ
environ.setdefault('DJANGO_SETTINGS_MODULE', "settings")
import django
SITE_URL = '127.0.0.1:8000'

django.setup()


def worker():
    r = redis.Redis()
    queue = SimpleQueue(r, 'queue')
    while True:
        print("Dequeue-ing")
        obj_json = queue.dequeue()
        requests.post('http://127.0.0.1:8000/notifications/save_to_database/', data={
            'data':obj_json
        })


if __name__ == '__main__':
    worker()
