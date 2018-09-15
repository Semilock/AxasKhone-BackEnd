from django.db import models

from core.post.models import Post
from core.user.models import Profile


class Notification(models.Model):
    type = models.CharField(max_length=100)
    object = models.ForeignKey(Profile, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name="received_notifs", on_delete=models.CASCADE)
    you = models.BooleanField(default=False)
    sender = models.ForeignKey(Profile, related_name="sent_notifs", on_delete=models.CASCADE)
    data = models.IntegerField(null=True, blank=True)
    """
    if the notif is about post(like & comment), it should contain post instance as well, 
    we put it in data field 
    """