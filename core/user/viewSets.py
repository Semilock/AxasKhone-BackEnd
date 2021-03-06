from rest_framework import viewsets, mixins
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, ListModelMixin

from core.user.models import Profile , UserFollow
from rest_framework.viewsets import GenericViewSet

from .serializers import ProfileSerializer
from core.mixins import LoggingMixin


class ProfileViewSet(LoggingMixin,
                     viewsets.GenericViewSet, UpdateModelMixin , RetrieveModelMixin, ListModelMixin ):

    queryset = Profile.objects.all()
    lookup_field = 'main_username'
    serializer_class = ProfileSerializer


class FollowerListViewSet(LoggingMixin,
                          mixins.ListModelMixin, GenericViewSet):
    queryset = UserFollow.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user_followers = UserFollow.objects.filter(destination=self.request.user.profile)
        return [item.source for item in user_followers]


class FollowingListViewSet(LoggingMixin,
                           mixins.ListModelMixin, GenericViewSet):
    queryset = UserFollow.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user_followers = UserFollow.objects.filter(source=self.request.user.profile)
        return [item.destination for item in user_followers]

