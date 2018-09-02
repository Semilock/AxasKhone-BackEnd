from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from .models import Post
from .serializers import PostSerializer

class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  # mixins.UpdateModelMixin,
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
