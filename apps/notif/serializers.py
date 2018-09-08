from rest_framework import serializers

from apps.notif.models import Notification


class NotifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
