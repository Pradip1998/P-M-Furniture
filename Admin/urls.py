from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name="Admin"
urlpatterns = [
    path('admin-login', views.Adminlogin.as_view(),name='admin-login'),
    path('admin-home', views.Adminhome,name='admin-home'),

    ]
