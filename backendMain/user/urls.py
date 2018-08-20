from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('change_password/', views.change_password, name='change_password'),
]