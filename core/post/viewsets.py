from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from .models import Post
from .serializers import PostSerializer, PostSerializerGET, PostSerializerPOST


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  # mixins.UpdateModelMixin,
                  # mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

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
    #

    # @action(methods='post', detail=True)
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

# class PostsViewSet(mixins.CreateModelMixin,
#                   mixins.RetrieveModelMixin,
#                   # mixins.UpdateModelMixin,
#                   # mixins.DestroyModelMixin,
#                   mixins.ListModelMixin,
#                   GenericViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#     def get_queryset(self):
#         return Post.objects.filter(profile=self.request.user.profile).order_by('-pk')