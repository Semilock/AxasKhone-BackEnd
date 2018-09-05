from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.utils.translation import gettext as _
from rest_framework.viewsets import GenericViewSet

from core.post.models import Favorite, Post


class AddToFavorites(APIView):
    def post(self, request):
        post_id = request.data.get("post_id")
        favorite_name = request.data.get("favorite")
        user = request.user
        favorites = Favorite.objects.get_or_create(title=favorite_name, profile=user.profile)
        favorites[0].posts.add(Post.objects.get(id=post_id))
        return Response({'status': _('succeeded')})
