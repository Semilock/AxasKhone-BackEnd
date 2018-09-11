import json

from django.shortcuts import render

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView, status

from apps.notif.models import Notification
from apps.notif.serializers import NotifSerializer
from core.post.models import Post
from core.user.models import Profile, UserFollow
from Redis.globals import *


@permission_classes((AllowAny,))
class SaveToDataBase(APIView):
    def post(self, request):
        if str(request.META.get("REMOTE_ADDR")) == "127.0.0.1":
            type = request.data.get("type")
            receiver = request.data.get("receiver")
            sender = request.data.get("sender")
            object = request.data.get("object")
            you = request.data.get("you")
            id = request.data.get("id")
            notif = Notification(type=type,
                                 receiver=Profile.objects.get(id=receiver),
                                 sender=Profile.objects.get(id=sender),
                                 object=Profile.objects.get(id=object),
                                 you=you)
            notif.save()
            if id > 0:
                notif.data = id
                notif.save()
            if type == follow_type:
                user_followers = UserFollow.objects.filter(destination=sender)
                # friends= [item.source for item in user_followers]
                for f in user_followers:
                    if not (f.source == receiver):
                        notif = Notification(type=type,
                                             receiver=f.source,
                                             sender=Profile.objects.get(id=sender),
                                             object=Profile.objects.get(id=object),
                                             you=False)
                        notif.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
