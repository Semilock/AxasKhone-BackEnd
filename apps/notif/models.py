from django.db import models


class Notification(models.Model):
    type = models.CharField(max_length=100)
    date_created = models.DateField(null=True)
    is_shown = models.BooleanField(False, null=True)