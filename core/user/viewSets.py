from rest_framework import viewsets
from rest_framework.mixins import UpdateModelMixin

# from delete_later.serializers import ProfileSerializerPost
from core.user.models import Profile


# class ProfileViewSet(viewsets.GenericViewSet, UpdateModelMixin ):
#
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializerPost


