from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.utils.translation import gettext as _

from core.post.models import Favorite, Post


class Favorites(APIView):
    def post(self, request):
        post_id = request.data.get("post_id")
        favorite_name = request.data.get("favorite")
        user = request.user
        if not user.id==(Post.objects.get(id=post_id)).user.id:
            return Response({'error': _('you can not add other users posts to your favorites')},
                            status=HTTP_400_BAD_REQUEST)
        favorites= Favorite.objects.get_or_create(title=favorite_name)
        favorites[0].posts.add(Post.objects.get(id=post_id))
        return Response({'status': _('succeeded')},
                        status=HTTP_400_BAD_REQUEST)

