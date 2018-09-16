from rest_framework import serializers

from apps.notif.models import Notification
from core.post.models import Post
from core.post.serializers import PostSerializerNOTIF
from core.user.serializers import ProfileSerializer


class NotifSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer()
    object = ProfileSerializer()
    post = serializers.SerializerMethodField()

    class Meta:
        model = Notification

        fields = ('type', 'you', 'sender', 'post', 'object')

    def get_post(self, obj):
        if not obj.data == None:
            return PostSerializerNOTIF(Post.objects.get(id=obj.data)).data
        else:
            return ""
