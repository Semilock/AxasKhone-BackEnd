#TODO : check home works correctly
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from core.user.models import Profile, UserFollow
from .models import Post, Favorite
from core.user.serializers import ProfileSerializer

from .models import Post
from .serializers import PostSerializerGET, PostSerializerPOST, FavoriteSerializer

class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  # mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    # lookup_field = 'main_username'
    queryset = Post.objects.all()
    serializer_class = PostSerializerGET

    def get_queryset(self):
        return Post.objects.filter(profile=self.request.user.profile).order_by('-pk')

    def perform_create(self, serializer):
        print(self.request.user.profile)
        serializer.save(profile=self.request.user.profile)


    def get_serializer_class(self):
        if self.request.method == 'GET' :
            return PostSerializerGET
        elif self.request.method == 'POST' :
            return PostSerializerPOST

    @action(methods=['GET'], detail=False)
    def list_post(self, request):
        username = request.GET.get('username')
        if not username:
            username = request.user.profile.main_username
        profile = Profile.objects.filter(main_username = username).first()
        if not( UserFollow.objects.filter(source=request.user.profile, destination=profile).exists() or profile.is_public or profile==request.user.profile ) :
            return Response({'error':'not_followed'},
                            status=HTTP_400_BAD_REQUEST)
        queryset = Post.objects.filter(profile__main_username = username)

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

class HomeViewSet(GenericViewSet, mixins.ListModelMixin, ):
    queryset = Post.objects.all()
    serializer_class = PostSerializerGET

    def get_queryset(self):
        posts = Post.objects.filter(profile__followers__source = self.request.user.profile).order_by('-pk')
        return posts
        # return [item.post for item in profiles]

class FavoriteViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):#todo ino yadat nare
        return Favorite.objects.filter(posts__user_id=self.request.user.id).distinct()

    # def retrieve(self, request, *args, **kwargs):
    #     list = Favorite.objects.filter(id=request.data.get('id'))
    #     print(list)
    #     serializer = self.get_serializer(list)
    #     return Response(serializer.data)
