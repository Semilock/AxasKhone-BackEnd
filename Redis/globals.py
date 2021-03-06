import redis

from Redis.redis_queue import SimpleQueue

conn = redis.Redis(decode_responses=True)
queue = SimpleQueue(conn, 'queue')

comment_type = 'comment'
like_type = 'like'
forgot_password_type = 'forgot'
invite_mail_type = 'invite_mail'
email_verification_type = 'verification'
follow_type = 'follow'
follow_request_type = 'follow_request'
unfollow_type = 'unfollow'
accept_follow_request_type = 'accept_follow_request'


