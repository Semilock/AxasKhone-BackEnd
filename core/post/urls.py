from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

from .viewsets import PostViewSet, FavoriteViewSet

# Routers provide an easy way of automatically determining the URL conf.
post_router = routers.DefaultRouter()
post_router.register(r'post', PostViewSet)

favarite_router = routers.DefaultRouter()
favarite_router.register(r'favorites', FavoriteViewSet)
#
# urlpatterns = [
#     url(r'^', include(router.urls)),
#     # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

urlpatterns = [
    path('', include(post_router.urls)),
    path('', include(favarite_router.urls))

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