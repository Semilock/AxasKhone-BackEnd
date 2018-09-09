import redis

from Redis.redis_queue import SimpleQueue

conn = redis.Redis()
queue = SimpleQueue(conn, 'queue')

comment_type = 'comment'
like_type = 'like'
follow_type = 'follow'
follow_request_type = 'follow_request'
accept_follow_request_type = 'accept_follow_request'


