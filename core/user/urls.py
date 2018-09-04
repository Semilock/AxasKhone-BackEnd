from django.conf.urls import url
from . import views
from django.urls import path, include

app_name = 'user'

urlpatterns = [
   url(r'^change_password/', views.ChangePassword.as_view(), name='change_password'),
   url(r'^profile_info/', views.ProfileInfo.as_view(), name='profile_info'),
   url(r'^invite_friends/', views.InviteFriends.as_view(), name='invite_friends'),
   url(r'^follow/' , views.Follow.as_view() , name='follow'),
   url(r'^accept/', views.Accept.as_view(), name='accept'),
   url(r'^follower_list/', views.FollowerList.as_view(), name='follower_lists'),
   url(r'^following_list/', views.FollowingList.as_view(), name='following_lists'),
   path('', include('core.post.urls'))
]

