from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Post, Favorite
from .serializers import PostSerializer, FavoriteSerializer


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  # mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-pk')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # @action(methods='post', detail=True)
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)


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