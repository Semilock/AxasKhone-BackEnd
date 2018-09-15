import re

bio_max_length = 200
caption_max_length = 620
favorite_title_max_length = 30
location_max_length = 30
tag_max_length = 60

comment_max_length = 520
username_max_length = 40
fullname_max_length = 40

email_pattern = re.compile("^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
username_pattern = re.compile("^[a-zA-Z][a-zA-Z.]+|[a-zA-Z_]+")
