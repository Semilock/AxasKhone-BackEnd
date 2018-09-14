from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.notif.models import Notification
from apps.notif.serializers import NotifSerializer


class NotifViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = NotifSerializer
    queryset = Notification.objects.all()

    def get_queryset(self):
        print(self.request.user.profile.main_username)
        return Notification.objects.filter(receiver_id=self.request.user.profile.id).order_by('-pk')