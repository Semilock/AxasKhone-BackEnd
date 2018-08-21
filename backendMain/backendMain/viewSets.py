from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin

from backendMain.serializers import ProfileSerializerPost
from user.models import Profile


class ProfileViewSet(viewsets.GenericViewSet, UpdateModelMixin ):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializerPost