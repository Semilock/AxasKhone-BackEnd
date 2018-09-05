from django.core.exceptions import ValidationError
from django.db import models
from core.user.models import User, Profile
import time
from os.path import splitext
from django.utils.translation import gettext as _


def user_directory_path(instance, filename):
    now_in_millisecs = int(round(time.time() * 1000))
    file_extension = splitext(filename)[1]
    return 'images/user_{0}/{1}{2}'.format(instance.user.id,
                                           now_in_millisecs,
                                           file_extension)


def validate_file_size(value):  # add this to some file where you can import it from
    limit = 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('File too large. Size should not exceed 2 MiB.'))


# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
# return 'media/images/user_{0}/{1}'.format(instance.user.id, filename)


class Post(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    # title = models.CharField(max_length=100, blank=False, null=False)  # TODO: change this?
    image = models.ImageField(upload_to=user_directory_path, blank=False, null=False,
                              validators=[validate_file_size])  # TODO: upload_to = ? etc
    caption = models.CharField(max_length=1500)
    # TODO: pub_date


class Favorite(models.Model):
    title = models.CharField(max_length=200)
    posts = models.ManyToManyField(Post)
    many = True

    def __str__(self):
        return str(self.posts.all())

