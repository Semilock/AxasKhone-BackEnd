from django.conf.urls import url
from rest_framework import routers

from core.post.views import AddToFavorites
from core.user.viewSets import FollowerListViewSet, FollowingListViewSet
from . import views
from django.urls import path, include

# app_name = 'user'

router = routers.DefaultRouter()
router.register(r'follower_list', FollowerListViewSet)
router.register(r'following_list', FollowingListViewSet)


urlpatterns = [
   url(r'^change_password/', views.ChangePassword.as_view(), name='change_password'),
   url(r'^profile_info/', views.ProfileInfo.as_view(), name='profile_info'),
   url(r'^invite_friends/', views.InviteFriends.as_view(), name='invite_friends'),
   url(r'^follow/' , views.Follow.as_view() , name='follow'),
   url(r'^accept/', views.Accept.as_view(), name='accept'),
   # url(r'^follower_list/', views.FollowerList.as_view(), name='follower_lists'),
   # url(r'^home/', views.Home.as_view(), name='follower_lists'),
   path('', include(router.urls)),
   path('', include('core.post.urls')),
   url(r'^add_to_favorites/', AddToFavorites.as_view())

]

