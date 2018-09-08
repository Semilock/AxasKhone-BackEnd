from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

from core.post.views import AddToTags
from .viewsets import PostViewSet, HomeViewSet, FavoriteViewSet, TagViewSet#, CommentViewSet

# Routers provide an easy way of automatically determining the URL conf.
home_router = routers.DefaultRouter()
favarite_router = routers.DefaultRouter()
tag_router = routers.DefaultRouter()
post_router = routers.DefaultRouter()
# comment_router = routers.DefaultRouter()
home_router.register(r'home', HomeViewSet)
favarite_router.register(r'favorites', FavoriteViewSet)
tag_router.register(r'tags', TagViewSet)
post_router.register(r'post', PostViewSet)
# comment_router.register(r'comment', CommentViewSet)


# urlpatterns = [
#     url(r'^', include(router.urls)),
#     # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

urlpatterns = [
    path('', include(post_router.urls)),
    path('', include(favarite_router.urls)),
    path('', include(home_router.urls)),
    path('', include(tag_router.urls)),
    # path('', include(comment_router.urls)),
        url(r'^add_to_tags/', AddToTags.as_view())

    # path(
    #     '',
    #     PostViewSet.as_view({'get': 'list'}), #{'get': 'list', 'post': 'create'}
    #     name='post-list',
    # ),
    # path(
    #     '<int:pk>/',
    #     PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
    #     name='post-detail',
    # ),
]




# from django.conf.urls import url, include
# from django.contrib.auth.models import User
# from django.urls import path
# from rest_framework import routers, serializers, viewsets
# from .models import Post
#
# # Serializers define the API representation.
# class PostSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Post
#         fields = ('image', 'text')
#
# # ViewSets define the view behavior.
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
# # Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'post', PostViewSet)
#
# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path(r'^', include(router.urls)),
#     # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]