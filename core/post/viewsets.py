from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from .models import Post
from .serializers import PostSerializer

# class c(APIVeiwSet)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save()

    # @action(methods='post', detail=True)
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

