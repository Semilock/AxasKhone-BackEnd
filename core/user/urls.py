from django.conf.urls import url
from . import views
from django.urls import path, include

# app_name = "user" # produces error: Could not resolve URL for hyperlinked relationship using view name "post-detail".
# You may have failed to include the related model in your API, or incorrectly configured the `lookup_field` attribute on this field.

urlpatterns = [
    url(r'^change_password/', views.ChangePassword.as_view(), name='change_password'),
    url(r'^profile_info/', views.ProfileInfo.as_view(), name='profile_info'),
    url(r'^invite_friends/', views.InviteFriends.as_view(), name='invite_friends'),
    url(r'^follow/' , views.Follow.as_view() , name='follow'),
    url(r'^accept/', views.Accept.as_view(), name='accept'),
    url(r'^follower_list/', views.FollowerList.as_view(), name='follower_lists'),
    url(r'^following_list/', views.FollowingList.as_view(), name='following_lists'),
    path('', include('core.post.urls')),
    path('forgot_password/', views.ForgotPassword.as_view()),
    path('reset_password/<str:uuidhex>/', views.ResetPassword.as_view())

]

