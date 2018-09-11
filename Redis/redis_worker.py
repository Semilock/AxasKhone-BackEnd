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
        queue.dequeue()

if __name__ == '__main__':
    worker()
