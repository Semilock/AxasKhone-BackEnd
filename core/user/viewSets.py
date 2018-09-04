from rest_framework import viewsets, mixins
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin

from core.user.models import Profile , UserFollow

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

    # class FollowerList(mixins.ListModelMixin):
    #     queryset = UserFollow.objects.all()
    #     serializer_class = Profile
    #
    #     def get_queryset(self):
    #         return UserFollow.objects.filter(destinations=self.context.get('request').user.profile)

    #
    # def retrieve(self, request, *args, **kwargs):
    #     super(ProfileViewSet, self).retrieve(request, *args, **kwargs)
    #     print("Stuff")