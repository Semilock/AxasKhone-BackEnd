
import time
from os.path import splitext

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from core.user.models import User, Profile


def user_directory_path(instance, filename):
    now_in_millisecs = int(round(time.time() * 1000))
    file_extension = splitext(filename)[-1] # [1] or [-1] ?
    return 'images/user_{0}/{1}{2}'.format(instance.profile.id,
                                           now_in_millisecs,
                                           file_extension)


def validate_size(value):  # add this to some file where you can import it from
    limit = 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('File too large. Size should not exceed 2 MiB.'))


# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
# return 'media/images/user_{0}/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
    text = models.CharField(max_length=100)
    number = models.IntegerField(default=0)



class Post(models.Model):
    profile = models.ForeignKey(Profile, blank=True, null=False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, blank=False, null=False,
                              validators=[validate_size])

    caption = models.CharField(max_length=600, blank=True)
    tag_string = models.CharField(max_length = 100, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts')
    location= models.CharField(max_length=40, blank=True)
    # TODO: pub_date

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)



class Comment(models.Model):
    text = models.CharField(max_length=600)
    profile = models.ForeignKey(Profile, blank=True, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True , blank=True)
    modified_at = models.DateTimeField(auto_now_add=True, blank=True)


class Like(models.Model):
    profile = models.ForeignKey(Profile, blank=True, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    title = models.CharField(max_length=40)
    posts = models.ManyToManyField(Post)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.posts.all())



