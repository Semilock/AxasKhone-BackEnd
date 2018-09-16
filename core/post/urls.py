from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

from core.post.views import AddToTags
from .viewsets import PostViewSet, HomeViewSet, FavoriteViewSet, TagViewSet, NameViewSet  # , CommentViewSet

home_router = routers.DefaultRouter()
favarite_router = routers.DefaultRouter()
tag_router = routers.DefaultRouter()
name_router = routers.DefaultRouter()
post_router = routers.DefaultRouter()
home_router.register(r'home', HomeViewSet)
favarite_router.register(r'favorites', FavoriteViewSet)
tag_router.register(r'tags', TagViewSet),
name_router.register(r'names', NameViewSet),
post_router.register(r'post', PostViewSet)


urlpatterns = [
    path('', include(post_router.urls)),
    path('', include(favarite_router.urls)),
    path('', include(home_router.urls)),
    path('', include(tag_router.urls)),
    path('', include(name_router.urls)),
    url(r'^add_to_tags/', AddToTags.as_view())
]