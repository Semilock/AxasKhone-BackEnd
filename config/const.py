import re

bio_max_length = 400
caption_max_length = 800

email_pattern = re.compile("^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
username_pattern = re.compile("^[a-zA-Z][a-zA-Z.]+|[a-zA-Z_]+")