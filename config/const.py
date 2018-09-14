import re

bio_max_length = 50
caption_max_length = 300

email_pattern = re.compile("^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
username_pattern = re.compile("^[a-zA-Z][a-zA-Z.]+|[a-zA-Z_]+")