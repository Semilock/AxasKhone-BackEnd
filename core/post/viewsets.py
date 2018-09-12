import queue
import random

from django.http import JsonResponse
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q
from Redis.globals import *
from apps.notif.models import Notification

from core.user.serializers import ProfileSerializer

from config.utils import LD
from .models import Post, Favorite, Tag, Comment, Like
from .serializers import PostSerializerGET, FavoriteSerializer, PostSerializerPOST, TagSerializer, CommentSerializer, \
    LikeSerializer
from core.user.models import Profile, UserFollow
from .models import Post, Favorite
from .models import Post
from .serializers import PostSerializerGET, FavoriteSerializer
from django.utils.translation import gettext as _


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
        image = request.FILES.get("image")
        if image is None:
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
        return Response({'status': _('succeeded')},
                        status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializerGET
        elif self.request.method == 'POST':
            return PostSerializerPOST

    @action(methods=['GET'], detail=False)
    def list_posts(self, request):
        username = request.GET.get('username')
        if not username:
            username = request.user.profile.main_username
        profile = Profile.objects.filter(main_username=username).first()
        if not (UserFollow.objects.filter(source=request.user.profile,
                                          destination=profile).exists() or profile.is_public or profile == request.user.profile):
            return Response({'error': 'not_followed'},
                            status=HTTP_400_BAD_REQUEST)
        queryset = Post.objects.filter(profile__main_username=username)

        posts = self.paginate_queryset(queryset)
        serializer_context = {
            'request': request,
        }
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
        if self.request.method == 'GET':
            queryset = Comment.objects.filter(post__pk=pk)
            comments = self.paginate_queryset(queryset)
            serializer = CommentSerializer(comments, many=True)
            return self.get_paginated_response(serializer.data)
        elif self.request.method == 'POST':
            text = request.data.get("text")
            if text is None or text == "":
                return JsonResponse({"error": "empty_field"}, status=HTTP_400_BAD_REQUEST)
            post = Post.objects.get(id=pk)
            profile = self.request.user.profile
            comment = Comment.objects.create(text=text, post=post, profile=profile)
            post.comments.add(comment)
            # queue.enqueue(create_comment_notif, post, profile)
            return Response({'status': _('succeeded')})

    @action(methods=['GET', 'POST'], detail=True)
    def like(self, request, pk):
        if self.request.method == 'GET':
            queryset = Like.objects.filter(post__pk=pk)
            likes = self.paginate_queryset(queryset)
            serializer = LikeSerializer(likes, many=True)
            return self.get_paginated_response(serializer.data)
        elif self.request.method == 'POST':
            post = Post.objects.get(id=pk)
            if post is None:
                return JsonResponse({"error": "post_not_find"}, status=HTTP_400_BAD_REQUEST)
            if Like.objects.filter(post=post, profile=self.request.user.profile).exists():
                return JsonResponse({"error": "already_liked"}, status=HTTP_400_BAD_REQUEST)
            profile = self.request.user.profile
            like = Like.objects.create(post=post, profile=profile)
            post.likes.add(like)
            queue.enqueue(create_like_notif, post, profile)
            return Response({'status': _('succeeded')})


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
        username = request.GET.get('username')
        print(username)
        if not username:
            username = request.user.profile.main_username
        serializer_context = {
            'request': request,
        }
        queryset = Favorite.objects.filter(profile__main_username=username)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FavoriteSerializer(page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = FavoriteSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def list_posts(self, request, pk):
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
        if page is not None:
            serializer = PostSerializerGET(page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializerGET(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def search(self, request):
        if(request.data.get('tag')==None):
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
        return Response({"results": result})

class NameViewSet(mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Tag.objects.all()

    @action(methods=['POST'], detail=False)
    def search(self, request):
        if (request.data.get('name') == None):
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
            query_list.append({"fullname": item.fullname, 'distance': distance})
        query_list=sorted(query_list, key= lambda x: x['distance'])[:30]
        result=[]
        for item in query_list:
            result.append(item['fullname'])
        return Response({"results": result})

        queryset_paginate = self.paginate_queryset(queryset)
        serializer = ProfileSerializer(queryset_paginate, context={'request': request}, many=True)
        return Response(serializer.data)
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


def create_comment_notif(post, profile):
    receiver = Profile.objects.get(id=post.profile.id)
    notif = Notification(type=comment_type, receiver=receiver, sender=profile, data=post, object=receiver)
    notif.you = True
    notif.save()
    # post_owner = Profile.objects.get(id=post.profile.id)
    # friends = post_owner.followers
    # for friend in friends:
    #     notif = Notification(type=comment_type, receiver=friend, sender=profile, data=post.id)
    #     notif.save()
    # n, created = Notification.objects.get_or_create(type=comment_type, receiver=post_owner, sender=profile, data=post.id)
    # n.you = True


def create_like_notif(post, profile):
    receiver = Profile.objects.get(id=post.profile.id)
    notif = Notification(type=like_type, receiver=receiver, sender=profile, data=post, object=receiver)
    notif.you = True
    notif.save()
