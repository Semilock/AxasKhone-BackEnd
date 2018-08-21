from django.conf.urls import url
from rest_framework import routers
from backendMain.viewSets import ProfileViewSet
from . import views




urlpatterns = {
    url(r'^register/', views.register, name='register'),
    # url(r'^', profilePatterns)
    # url(r'^change_password/', views.change_password, name='change_password'
}