from rest_framework import serializers

from apps.notif.models import Notification
from core.post.models import Post
from core.post.serializers import PostSerializerGET
from core.user.serializers import ProfileSerializerNotif, ProfileSerializer


class NotifSerializer(serializers.ModelSerializer):
    receiver = ProfileSerializer()
    sender = ProfileSerializer()
    object = ProfileSerializer()
    data = serializers.SerializerMethodField()
    class Meta:
        model = Notification
        # fields = ('type', 'is_shown', 'receiver', 'you', 'sender', 'object')

        fields = ('type', 'is_shown', 'receiver', 'you', 'sender', 'data', 'object')

    def get_data(self, obj):
        if not obj.data==None:
            return Post.objects.get(id= obj.data)
        else:
            return ""