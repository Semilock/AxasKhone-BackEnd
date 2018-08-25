from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#TODO: followers and following list should add
#TODO: profile pic should add to profile info

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length = 200, blank = True)
    bio = models.CharField(max_length=400, blank=True)
    profile_pic = models.ImageField(max_length = 500, blank = True)
    followers_number = models.IntegerField(default=0, blank = True)
    following_number = models.IntegerField(default=0, blank = True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
