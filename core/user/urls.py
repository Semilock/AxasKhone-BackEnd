from django.conf.urls import url
from . import views

urlpatterns = [

   url(r'^profile_info/', views.ProfileInfo.as_view(), name='profile_info')
]

