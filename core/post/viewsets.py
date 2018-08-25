from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from .models import Post
from .serializers import PostSerializer

# class c(APIVeiwSet)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # @action(methods='post', detail=True)
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

