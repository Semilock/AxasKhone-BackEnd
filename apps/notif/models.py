from django.db import models

from core.user.models import Profile


class Notification(models.Model):
    type = models.CharField(max_length=100)
    object = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_shown = models.BooleanField(default=False)
    receiver = models.ForeignKey(Profile, related_name="received_notifs", on_delete=models.CASCADE)
    you = models.BooleanField(default=False)
    sender = models.ForeignKey(Profile, related_name="sent_notifs", on_delete=models.CASCADE)
    data = models.IntegerField(null=True, blank=True)
    """
    if the notif is about post, it should contain postID, 
    we put it in data field 
    """