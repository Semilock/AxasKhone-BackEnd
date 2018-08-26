from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core.user import views
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.user.viewSets import ProfileViewSet

router = SimpleRouter()
router.register('user/profile_info' , ProfileViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('', include('core.post.urls')),
    # url(r'^', include(router.urls)),
    # url(r'^user/', include('core.user.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', TokenObtainPairView.as_view()),
    url(r'^refresh/', TokenRefreshView.as_view()),
    url(r'^register/', views.Register.as_view()),
    # url(r'^login/', views.Login.as_view()),
    url(r'^register_complement/', views.RegisterComplementView.as_view()),
] + router.urls
