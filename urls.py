from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from rest_framework import routers
from django.conf import settings
from core.user import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.user.viewSets import ProfileViewSet


router = routers.DefaultRouter()
router.register('profile_info' , ProfileViewSet)

urlpatterns = [
                  # url(r'^', include(router.urls)),
                  url(r'^user/', include('core.user.urls')),
                  url(r'^notifications/', include('apps.notif.urls')),
                  url(r'^admin/', admin.site.urls),
                  url(r'^login/', TokenObtainPairView.as_view()),
                  url(r'^refresh/', TokenRefreshView.as_view()),
                  url(r'^register/', views.Register.as_view()),
                  url(r'^register_validation/', views.RegisterValidation.as_view()),

] + router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # TODO