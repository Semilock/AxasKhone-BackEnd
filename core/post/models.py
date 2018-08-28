from django.db import models
from core.user.models import User, Profile
import time
from os.path import splitext


def user_directory_path(instance, filename):
    now_in_millisecs = int(round(time.time() * 1000))
    file_extension = splitext(filename)[1]
    return 'media/images/user_{0}/{1}{2}'.format(instance.user.id,
                                                 now_in_millisecs,
                                                 file_extension)

    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # return 'media/images/user_{0}/{1}'.format(instance.user.id, filename)


class Post(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)  # TODO: change this?
    image = models.ImageField(upload_to=user_directory_path, blank=False, null=True)  # TODO: upload_to = ? etc
    text = models.CharField(max_length=1500)
    # TODO: time