from django.conf.urls import url

from . import views




urlpatterns = {

    url(r'^change_password/', views.change_password, name='change_password'),
    url(r'^profile_info/', views.profile_info, name='profile_info')
}
