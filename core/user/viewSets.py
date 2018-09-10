from rest_framework import viewsets, mixins
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, ListModelMixin

from core.user.models import Profile , UserFollow
from rest_framework.viewsets import GenericViewSet

from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.GenericViewSet, UpdateModelMixin , RetrieveModelMixin, ListModelMixin ):

    queryset = Profile.objects.all()
    lookup_field = 'main_username'
    serializer_class = ProfileSerializer
    #
    # def get_serializer_class(self):
    #     if self.request.method == 'PUT' :
    #         return ProfileSerializer
    #     elif self.request.method == 'GET' :
    #         return ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        super(ProfileViewSet, self).retrieve(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     queryset = list(self.filter_queryset(self.get_queryset()))
    #
    #     queryset= sorted(queryset, key=lambda x: -x.follower_number())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return self.get_paginated_response(serializer.data)
    #
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

