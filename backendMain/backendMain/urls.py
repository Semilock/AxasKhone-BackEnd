from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import verify_jwt_token ,obtain_jwt_token

from user import views

urlpatterns = {
    url(r'^user/', include('user.urls')),
    url(r'^login/', obtain_jwt_token),
    url(r'^register/', views.register),
    url(r'^admin/', admin.site.urls),
    # url(r'^register-complement/', views.UserViewSet.as_view({'post': 'update'})),
    url(r'^api-token-verify/', verify_jwt_token),
}
