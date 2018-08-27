from rest_framework import viewsets
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin

from core.user.models import Profile
from .serializers import ProfileSerializerPost, ProfileSerializerGet


class ProfileViewSet(viewsets.GenericViewSet, UpdateModelMixin , RetrieveModelMixin ):

    queryset = Profile.objects.all()
    lookup_field = 'main_username'
    serializer_class = ProfileSerializerPost

    def get_serializer_class(self):
        if self.request.method == 'PUT' :
            return ProfileSerializerPost
        elif self.request.method == 'GET' :
            return ProfileSerializerGet


    
    def retrieve(self, request, *args, **kwargs):
        super(ProfileViewSet, self).retrieve(request, *args, **kwargs)
        print("Stuff")