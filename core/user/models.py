from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from core.user.models import User
import time
from os.path import splitext


# TODO: followers and following list should add
# TODO: profile pic should add to profile info
def profile_pic_directory_path(instance, filename):
    now_in_millisecs = int(round(time.time() * 1000))
    file_extension = splitext(filename)[1]
    return 'profile_photos/user_{0}/{1}{2}'.format(instance.user.id,
                                                 now_in_millisecs,
                                                 file_extension)


class Profile(models.Model):
    main_username = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200, blank=True)
    bio = models.CharField(max_length=400, blank=True)
    profile_pic = models.ImageField(upload_to=profile_pic_directory_path, blank=True, null=True)
    followers_number = models.IntegerField(default=0, blank=True)
    following_number = models.IntegerField(default=0, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
