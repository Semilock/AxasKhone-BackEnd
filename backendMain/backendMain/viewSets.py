from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import UpdateModelMixin

from backendMain.serializers import ProfileSerializerPost
from user.models import Profile


@api_view(["POST"])
class ProfileViewSet(viewsets.GenericViewSet, UpdateModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializerPost


