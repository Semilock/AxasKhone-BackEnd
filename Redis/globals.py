import redis

from Redis.redis_queue import SimpleQueue

conn = redis.Redis()
queue = SimpleQueue(conn, 'queue')

comment_type = 'comment'
like_type = 'like'
