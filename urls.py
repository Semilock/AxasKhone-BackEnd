from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

# from core.user.viewSets import ProfileViewSet

# router = routers.DefaultRouter()
# router.register(r'register-complement', ProfileViewSet)


urlpatterns = [
    path('', include('core.post.urls')),

    # url(r'^', include(router.urls)),
    # url(r'^user/', include('cor.user.urls')),
    url(r'^api_token_verify/', verify_jwt_token),
    url(r'^api_token_refresh/', refresh_jwt_token),
    url(r'^login/', obtain_jwt_token),
    url(r'^login/', obtain_jwt_token),
    url(r'^admin/', admin.site.urls),

    # url(r'^register/', views.Register.as_view()),
    # url(r'^login/', views.Login.as_view()),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    # url(r'^user_api/', views.UsersViewApi.as_view()),  # for test
    # url(r'^register-complement/', ),
    # url(r'^register-complement/', ProfileViewSet.),

    # url(r'^register/', views.register),
    # url(r'^register_complement/', views.RegisterComplementView.as_view()),
]
