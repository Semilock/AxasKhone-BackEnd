from django.conf.urls import url
from rest_framework import routers

from django.urls import path, include

from apps.notif.viewsets import NotifViewSet

router = routers.DefaultRouter()
router.register(r'', NotifViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

