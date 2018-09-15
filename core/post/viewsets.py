#TODO: tag ha ba post zakhire nemishan!!!
import json
import logging
import random

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from config.utils import now_ms, req_log_message, res_log_message

logger = logging.getLogger(__name__)
from Redis.globals import *
from apps.notif.models import Notification
from apps.notif.serializers import NotifSerializer

from core.user.serializers import ProfileSerializer

from config.utils import LD
from .models import Post, Favorite, Tag, Comment, Like
from .serializers import PostSerializerGET, FavoriteSerializer, PostSerializerPOST, TagSerializer, CommentSerializer, \
    LikeSerializer
from core.user.models import Profile, UserFollow
from core.user.serializers import ProfileSerializer
from django.db.models import Q
from .models import Favorite
from .models import Post
from .models import Tag, Comment, Like
from .serializers import PostSerializerGET, FavoriteSerializer
from .serializers import PostSerializerPOST, TagSerializer, CommentSerializer, \
    LikeSerializer


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  # mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializerGET

    def get_queryset(self):
        return Post.objects.filter(profile=self.request.user.profile).order_by('-pk')

    def perform_create(self, serializer):
        # print(self.request.user.profile)
        serializer.save(profile=self.request.user.profile)

    def create(self, request, *args, **kwargs):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        image = request.FILES.get("image")
        if image is None:
            log_result = 'user id={0} tried to create a post without any iamge.'.format(request.user.id)
            log_message = res_log_message(request, log_result, req_time)
            logger.warning(log_message)
            return Response({'error': _('image is required')},
                            status=HTTP_400_BAD_REQUEST)
        caption = request.POST.get("caption")
        location = request.POST.get("location")
        profile = request.user.profile
        post = Post.objects.create(image=image, caption=caption, location=location, profile=profile)
        tag_string = request.POST.get("tag_string")
        tag_list = str(tag_string).split()
        for tag in tag_list:
            t, is_created = Tag.objects.get_or_create(text=tag)
            post.tags.add(t)
        log_result = 'user id={0} created a new post(id={1}).'.format(request.user.id, post.id)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return Response({'status': _('succeeded')},
                        status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializerGET
        elif self.request.method == 'POST':
            return PostSerializerPOST

    @action(methods=['GET'], detail=False)
    def list_posts(self, request):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        username = request.GET.get('username')
        if not username:
            username = request.user.profile.main_username
        profile = Profile.objects.filter(main_username=username).first()
        if not (UserFollow.objects.filter(source=request.user.profile,
                                          destination=profile).exists() or profile.is_public or profile == request.user.profile):
            log_result = 'user(id={0}) requested to get lists of posts of user(id={1}) while not following him'\
                .format(request.user.id, profile.user.id)
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return Response({'error': 'not_followed'},
                            status=HTTP_400_BAD_REQUEST)
        queryset = Post.objects.filter(profile__main_username=username)

        posts = self.paginate_queryset(queryset)
        serializer_context = {
            'request': request,
        }
        log_result = 'list posts of user(id={0})'.format(profile.user.id)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        if posts is not None:
            serializer = PostSerializerGET(posts, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializerGET(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    # @action(methods='post', detail=True)
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

    @action(methods=['GET', 'POST'], detail=True)
    def comment(self, request, pk):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        if self.request.method == 'GET':
            queryset = Comment.objects.filter(post__pk=pk)
            comments = self.paginate_queryset(queryset)
            serializer = CommentSerializer(comments, many=True, context={'request': request} )
            log_result = 'user(id={0}) requested for comments on post(id={1})'.format(request.user.id, pk)
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return self.get_paginated_response(serializer.data)
        elif self.request.method == 'POST':
            text = request.data.get("text")
            if text is None or text == "":
                return JsonResponse({"error": "empty_field"}, status=HTTP_400_BAD_REQUEST)
            post = Post.objects.get(id=pk)
            profile = self.request.user.profile
            comment = Comment.objects.create(text=text, post=post, profile=profile)
            post.comments.add(comment)
            receiver = Profile.objects.get(id=post.profile.id)
            # notif = Notification(type=comment_type, receiver=receiver, sender=profile, object=receiver, you=True)
            data = {"type": comment_type,
                    "receiver": receiver.id,
                    "sender": profile.id,
                    "you": True,
                    "object": receiver.id,
                    "id": post.id
                    }
            queue.enqueue(json.dumps(data))
            log_result = 'user(id={0}) added a new comment on post(id={1}).Queued on redis.'.format(request.user.id,post.id)
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return Response({'status': _('succeeded')})

    @action(methods=['GET', 'POST'], detail=True)
    def like(self, request, pk):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        if self.request.method == 'GET':
            queryset = Like.objects.filter(post__pk=pk)
            likes = self.paginate_queryset(queryset)
            serializer = LikeSerializer(likes, many=True, context={'request': request} )
            log_result = 'user(id={0}) requested for likes on post(id={1})'.format(request.user, pk)
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return self.get_paginated_response(serializer.data)
        elif self.request.method == 'POST':
            post = Post.objects.get(id=pk)
            if post is None:
                log_result = 'post not found: user(id={0}) requested to like post(id={1}).'.format(request.user.id, post.id)
                log_message = res_log_message(request, log_result, req_time)
                logger.warning(log_message)
                return JsonResponse({"error": "post_not_find"}, status=HTTP_400_BAD_REQUEST)
            if Like.objects.filter(post=post, profile=self.request.user.profile).exists():
                Like.objects.get(post=post, profile=self.request.user.profile).delete()
                log_result = 'user(id={0}) unliked post(id={1}).'.format(request.user.id, post.id)
                log_message = res_log_message(request, log_result, req_time)
                logger.info(log_message)
                return Response({'status': _('unliked')})
            profile = self.request.user.profile
            like = Like.objects.create(post=post, profile=profile)
            post.likes.add(like)
            receiver = Profile.objects.get(id=post.profile.id)
            data = {"type": like_type,
                    "receiver": receiver.id,
                    "sender": profile.id,
                    "you": True,
                    "object": receiver.id,
                    "id": post.id
                    }
            queue.enqueue(json.dumps(data))
            log_result = 'user(id={0}) liked post(id={1}).Queued on redis.'.format(request.user.id,post.id)
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return Response({'status': _('succeeded')})
    #
    # def unlike(self, request, pk):
    #     post = Post.objects.get(id=pk)
    #     if post is None:
    #         return JsonResponse({"error": "post_not_find"}, status=HTTP_400_BAD_REQUEST)
    #     if Like.objects.filter(post=post, profile=self.request.user.profile).exists():
    #         Like.objects.get(post=post, profile=self.request.user.profile).delete()
    #         return Response({'status': _('succeeded')})
    #     return Response({"error": "already unliked"})



class HomeViewSet(GenericViewSet, mixins.ListModelMixin, ):
    queryset = Post.objects.all()
    serializer_class = PostSerializerGET

    def get_queryset(self):
        posts = Post.objects.filter(Q(profile__followers__source=self.request.user.profile) | Q(
            profile=self.request.user.profile)).distinct().order_by('-pk')
        return posts
        # return [item.post for item in profiles]


class FavoriteViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(profile__user=self.request.user)

    @action(methods=['GET'], detail=False)
    def list_favorites(self, request):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        username = request.GET.get('username')
        print(username)
        if not username:
            username = request.user.profile.main_username
        serializer_context = {
            'request': request,
        }
        queryset = Favorite.objects.filter(profile__main_username=username)
        page = self.paginate_queryset(queryset)
        log_result = 'user id={0} requested to receive lists of favorites of user(id={1})'.format(request.user.id,User.objects.get(profile__main_username=username))
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        if page is not None:
            serializer = FavoriteSerializer(page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = FavoriteSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def list_posts(self, request, pk):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        username = request.GET.get('username')
        if not username:
            username = request.user.id
        favorite = Favorite.objects.get(id=pk)

        queryset = favorite.posts.filter(
            Q(profile__is_public=True) | Q(profile__followers__source=self.request.user.profile) | Q(
                profile__user=request.user))
        # .filter(user_id=user_id)

        page = self.paginate_queryset(queryset)
        serializer_context = {
            'request': request,
        }
        log_result = 'user id={0} requested for list of posts of favorite(id={1}).'.format(request.user.id, pk)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        if page is not None:
            serializer = PostSerializerGET(page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializerGET(queryset, many=True, context=serializer_context)
        return Response(serializer.data)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = list(sorted(Tag.objects.all().order_by('-number')[:20], key=lambda x: random.random()))
        return queryset

    @action(methods=['GET'], detail=False)
    def list_posts(self, request):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        # if not username:
        #     username = request.user.id
        tag = Tag.objects.get(text=request.GET.get('tag'))

        queryset = tag.posts.filter(
            Q(profile__is_public=True) | Q(profile__followers__source=self.request.user.profile) | Q(
                profile__user=request.user))

        page = self.paginate_queryset(queryset)
        serializer_context = {
            'request': request,
        }
        log_result = 'user id={0} requested for list of posts of tag "{1}".'.format(request.user.id, tag.text)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        if page is not None:
            serializer = PostSerializerGET(page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializerGET(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def search(self, request):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        if(request.data.get('tag')==None or request.data.get('tag') =="" or request.data.get('tag') ==" "):
            log_result = 'empty field error in search'
            log_message = res_log_message(request, log_result, req_time)
            logger.warning(log_message)
            return Response({"error":"empty_field"})
        pattern_set = request.data.get('tag').split()
        query = Q()
        for pattern in pattern_set:
            query = query | Q(text__contains=pattern)
        queryset = Tag.objects.filter(query).distinct().order_by('number')  # TODO: order by (number used)

        query_list = []
        for item in queryset:
            distance = len(str(item.text))
            for pattern in pattern_set:
                distance = min(LD(item.text, pattern), distance)
            query_list.append({"text": item.text, 'distance': distance})
        query_list = sorted(query_list, key=lambda x: x['distance'])[:30]
        result = []
        for item in query_list:
            result.append(item['text'])
        log_result = 'user(id={0}) searched in tags'.format(request.user.id)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return Response({"results": result})

class NameViewSet(mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Tag.objects.all()

    @action(methods=['POST'], detail=False)
    def search(self, request):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        if (request.data.get('name') == None or request.data.get('name') =="" or request.data.get('name') ==" "):
            log_result = 'empty field error in search'
            log_message = res_log_message(request, log_result, req_time)
            logger.warning(log_message)
            return Response({"error":"empty_field"})
        pattern_set = request.data.get('name').split()
        query = Q()
        for pattern in pattern_set:
            query = query | Q(fullname__contains=pattern)
        queryset = Profile.objects.filter(query).distinct()

        query_list = []
        for item in queryset:
            distance = len(str(item.fullname))
            for pattern in pattern_set:
                distance = min(LD(item.fullname, pattern), distance)
            query_list.append({"profile": item, 'distance': distance})
        query_list=sorted(query_list, key= lambda x: x['distance'])[:30]
        result=[]
        for item in query_list:
            profile= ProfileSerializer(item["profile"], context={'request': request})
            result.append(profile.data)
        log_result = 'user(id={0}) searched in users names'.format(request.user.id)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return Response({"results": result})

        # queryset_paginate = self.paginate_queryset(queryset)
        # serializer = ProfileSerializer(queryset_paginate, context={'request': request}, many=True)
        # return Response(serializer.data)
        # serializer = []
        # for item in queryset_paginate:
        #     serializer.append(item.main_username)
        # return self.get_paginated_response(serializer)
        #  #ALGORITHM DISTANCE


# class CommentViewSet(mixins.CreateModelMixin,
#                   mixins.RetrieveModelMixin,
#                   #mixins.UpdateModelMixin,
#                   # mixins.DestroyModelMixin,
#                   mixins.ListModelMixin,
#                   GenericViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
#     def get_queryset(self):
#         return Comment.objects.filter(profile=self.request.user.profile)
#
#     @action(methods=['GET'], detail=True)
#     def get_comment(self, request, pk):
#         queryset = Comment.objects.filter(post__pk=pk)
#         comments = self.paginate_queryset(queryset)
#         serializer = CommentSerializer(comments, many=True)
#         return self.get_paginated_response(serializer.data)
#
#     @action(methods=['POST'], detail=True)
#     def add_comment(self, request, pk):
#         # pk = request.GET.get("pk")
#         text = request.data.get("text")
#         post = Post.objects.get(id=pk)
#         comment = Comment.objects.create(text=text, post=post, profile=self.request.user.profile)
#         post.comments.add(comment)
#         return Response({'status': ('succeeded')})
