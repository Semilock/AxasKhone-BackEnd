from django.conf.urls import url

from . import views

urlpatterns = {
    url(r'^register/', views.register, name='register'),
    url(r'^register-complement/', views.UserViewSet.as_view({'post': 'update'})),
}