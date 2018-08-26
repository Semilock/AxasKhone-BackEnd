from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
# from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

# from core.user.viewSets import ProfileViewSet

# router = routers.DefaultRouter()
# router.register(r'register-complement', ProfileViewSet)
from django.conf import settings
from core.user import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', include('core.post.urls')),
    # url(r'^', include(router.urls)),
    # url(r'^user/', include('cor.user.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', TokenObtainPairView.as_view()),
    url(r'^refresh/', TokenRefreshView.as_view()),
    url(r'^register/', views.Register.as_view()),
    # url(r'^login/', views.Login.as_view()),
    url(r'^register_complement/', views.RegisterComplementView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # TODO
