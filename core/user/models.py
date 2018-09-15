from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import time
from os.path import splitext
import uuid
from django.utils import timezone
import datetime as datetime_module
from hashlib import sha256

# TODO: followers and following list should add
# TODO: profile pic should add to profile info
from django.utils.datetime_safe import datetime

# from core.user import serializers
from config.const import bio_max_length


def profile_pic_directory_path(instance, filename):
    now_in_millisecs = int(round(time.time() * 1000))
    file_extension = splitext(filename)[-1]
    return 'profile_photos/user_{0}/{1}{2}'.format(instance.id,
                                                 now_in_millisecs,
                                                 file_extension)


class Profile(models.Model):
    main_username = models.CharField(max_length=50, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50, blank=True)
    bio = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(upload_to=profile_pic_directory_path, blank=True, null=True)
    is_public = models.BooleanField(default=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=True, blank=False, null=False)
    #todo must change into false for default value


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserFollow(models.Model):
    source = models.ForeignKey(Profile, related_name='followings', on_delete=models.CASCADE)
    destination = models.ForeignKey(Profile, related_name = 'followers', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        index_together = [
            ('source', 'created_at'),
            ('destination', 'created_at'),
        ]

class UserFollowRequest(models.Model):
    source = models.ForeignKey(Profile, related_name='sender', on_delete=models.CASCADE)
    destination = models.ForeignKey(Profile, related_name = 'reciver', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        index_together = [
            ('source', 'created_at'),
            ('destination', 'created_at'),
        ]


class PasswordResetRequests(models.Model):
    user = models.OneToOneField(User, primary_key=True, blank=False, null=False, on_delete=models.CASCADE)
    # uuid = models.UUIDField(primary_key=True,
    #                         default=uuid.uuid4, editable=False) #  TODOdone: hash it later
    hashed_token = models.BinaryField(max_length=32, null=False, blank=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def hash_token(token):
        """
        Takes a string, hashes it and returns the resulted bytes.
        :param token: ASCII string
        :return: bytes string of length at most 32
        """
        hashed_token = sha256(token.encode('ascii'))
        hashed_token = hashed_token.digest()[:min(hashed_token.digest_size, 32)]
        return hashed_token

    def set_token(self, token):
        hashed_token = PasswordResetRequests.hash_token(token)
        self.hashed_token = hashed_token

    # seems redundant
    # def token_verified(self, token):
    #     hashed_token = PasswordResetRequests.hash_token(token)
    #     return self.token == hashed_token

    def expired(self):
        # test
        # print("req_date")
        # print(self.req_date)
        # print("now")
        # print(timezone.now())
        # test
        return self.created_at < timezone.now() - datetime_module.timedelta(days=1)


class EmailVerificationRequests(models.Model):
    profile = models.OneToOneField(Profile, primary_key=True, blank=False, null=False, on_delete=models.CASCADE)
    # uuid = models.UUIDField(primary_key=True,
    #                         default=uuid.uuid4, editable=False) #  TODOdone: hash it later
    hashed_token = models.BinaryField(max_length=32, null=False, blank=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def hash_token(token):
        """
        Takes a string, hashes it and returns the resulted bytes.
        :param token: ASCII string
        :return: bytes string of length at most 32
        """
        hashed_token = sha256(token.encode('ascii'))
        hashed_token = hashed_token.digest()[:min(hashed_token.digest_size, 32)]
        return hashed_token

    def set_token(self, token):
        hashed_token = PasswordResetRequests.hash_token(token)
        self.hashed_token = hashed_token

    def expired(self):
        return self.created_at < timezone.now() - datetime_module.timedelta(minutes=30)