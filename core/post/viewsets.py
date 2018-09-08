# TODO: tag ha ba post zakhire nemishan!!!
import redis
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q

from Redis.globals import queue, comment_type
from apps.notif.models import Notification
from .models import Post, Favorite, Tag, Comment
from .serializers import PostSerializerGET, FavoriteSerializer, PostSerializerPOST, TagSerializer, CommentSerializer

from core.user.models import Profile, UserFollow
from .models import Post, Favorite
from core.user.serializers import ProfileSerializer

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
            post = Post.objects.get(id=pk)
            queue.enqueue(create_comment, post, text, self.request.user.profile) # added by arghavan
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
        return Tag.objects.all()

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


def create_comment(post, text, profile):
    notif = Notification(type = comment_type)
    notif.save()
    comment = Comment.objects.create(notif=notif,text=text, post=post, profile=profile)
    post.comments.add(comment)

