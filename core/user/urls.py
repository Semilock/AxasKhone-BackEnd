from django.conf.urls import url
from . import views

urlpatterns = {

    url(r'^change_password/', views.ChangePassword.as_view(), name='change_password'),
    url(r'^profile_info/', views.ProfileInfo.as_view(), name='profile_info')
}

