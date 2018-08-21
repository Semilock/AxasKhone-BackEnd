from django.conf.urls import url

from . import views

urlpatterns = {

    url(r'^register/', views.register, name='register'),
    # url(r'^change_password/', views.change_password, name='change_password'),
    # url(r'^register-complement/', views.UserViewSet.as_view({'post': 'update'})),
    url(r'^change_password/', views.change_password, name='change_password')
}
