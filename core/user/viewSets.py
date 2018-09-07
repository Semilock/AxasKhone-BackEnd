from rest_framework import viewsets, mixins
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin

from core.user.models import Profile , UserFollow
from rest_framework.viewsets import GenericViewSet

from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.GenericViewSet, UpdateModelMixin , RetrieveModelMixin ):

    queryset = Profile.objects.all()
    lookup_field = 'main_username'
    serializer_class = ProfileSerializer

    # def get_serializer_class(self):
    #     if self.request.method == 'PUT' :
    #         return ProfileSerializer
    #     elif self.request.method == 'GET' :
    #         return ProfileSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     super(ProfileViewSet, self).retrieve(request, *args, **kwargs)
    #     # print("Stuff")



class FollowerListViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = UserFollow.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user_followers = UserFollow.objects.filter(destination=self.request.user.profile)
        return [item.source for item in user_followers]


class FollowingListViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = UserFollow.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user_followers = UserFollow.objects.filter(source=self.request.user.profile)
        return [item.destination for item in user_followers]
