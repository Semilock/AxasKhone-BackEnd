# Create your views here.
import logging

from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import now_ms, req_log_message, res_log_message
from core.post.models import Favorite, Post, Tag

logger = logging.getLogger(__name__)

class AddToFavorites(APIView):
    def post(self, request):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        post_id = request.data.get("post_id")
        favorite_name = request.data.get("favorite")
        user = request.user
        favorites = Favorite.objects.get_or_create(title=favorite_name, profile=user.profile)
        favorites[0].posts.add(Post.objects.get(id=post_id))
        log_result = 'Post(id={0}) added to favorite (id={1}.'.format(post_id, favorites[0].id)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return Response({'status': _('succeeded')})

class RemoveFromFavorites(APIView):
    def post(self, request):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        favorite_id = request.data.get("favorite_id")
        Favorite.objects.get(id=favorite_id).delete()
        log_result = 'favorite (id={0}) removed from favorite list'.format(favorite_id)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return Response({'status': _('succeeded')})


class AddToTags(APIView):
    def post(self, request):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        post_id = request.data.get("post_id")
        tag_text = request.data.get("tag")
        post = Post.objects.get(id=post_id)

        # post=Post.objects.get(post_id=post_id)
        # if post.profile.user != request.user
        #     return({({'error': _('you cant add tag to others post)},
        #                     status=HTTP_400_BAD_REQUEST)})
        tags = Tag.objects.get_or_create(text=tag_text)
        tags[0].posts.add(post)
        post.tags.add(tags[0])
        log_result = 'tag (text={0}) added to Post (id={1}).'.format(tag_text, post_id)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return Response({'status': _('succeeded')})
