from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import verify_jwt_token ,obtain_jwt_token, refresh_jwt_token

from backendMain.viewSets import ProfileViewSet
from user import views

# router = routers.DefaultRouter()
# router.register(r'register-complement', ProfileViewSet)


urlpatterns = {
    # url(r'^', include(router.urls)),
    url(r'^user/', include('user.urls')),
    url(r'^login/', obtain_jwt_token),
    url(r'^admin/', admin.site.urls),
    url(r'^api_token_verify/', verify_jwt_token),
    url(r'^api_token_refresh/', refresh_jwt_token),
    url(r'^register/', views.register),
    url(r'^register_complement/', views.RegisterComplementView.as_view()),
}
