from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.create_user_collection, name="home"),
    path('add/', views.add_user, name="useradd"),
]
