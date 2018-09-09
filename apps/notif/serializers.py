from rest_framework import serializers

from apps.notif.models import Notification
from core.user.serializers import ProfileSerializer


class NotifSerializer(serializers.ModelSerializer):
    receiver = ProfileSerializer()
    sender = ProfileSerializer()
    object = ProfileSerializer()
    class Meta:
        model = Notification
        fields = ('type', 'is_shown', 'receiver', 'you', 'sender', 'data', 'object')