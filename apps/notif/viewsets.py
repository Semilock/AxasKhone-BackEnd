from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.notif.models import Notification
from apps.notif.serializers import NotifSerializer


class NotifViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = NotifSerializer
    queryset = Notification.objects.all()

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user.profile).order_by('-pk')