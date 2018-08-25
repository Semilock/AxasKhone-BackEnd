from django.db import models
from user.models import User
# from backendMain.user.models import Profile


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Post(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)  # TODO: on_delete = ?
    image = models.ImageField(upload_to=user_directory_path, null=True)  # TODO: upload_to = ? etc
    text = models.CharField(max_length=1500)
