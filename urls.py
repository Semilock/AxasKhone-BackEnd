from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from django.conf import settings
from src.core.user import views
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from src.core.user.viewSets import ProfileViewSet

router = SimpleRouter()
router.register('user/profile_info', ProfileViewSet)

urlpatterns = router.urls

urlpatterns = [
                  path('', include('src.core.post.urls')),
                  # url(r'^', include(router.urls)),
                  # url(r'^user/', include('core.user.urls')),
                  url(r'^admin/', admin.site.urls),
                  url(r'^login/', TokenObtainPairView.as_view()),
                  url(r'^refresh/', TokenRefreshView.as_view()),
                  url(r'^register/', views.Register.as_view()),
                  # url(r'^login/', views.Login.as_view()),
                  url(r'^register_complement/', views.RegisterComplementView.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urls  # TODO
