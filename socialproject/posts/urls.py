from django.contrib import admin
from django.urls import path 
from . import views
from django.contrib.auth import views as auth_view


urlpatterns = [
    path("create/",views.post_create,name="create"),
    path('feed',views.feed,name="feed"),
    path("like",views.like_post , name='like'),
    path("<int:post_id>/delete/", views.post_delete, name="post_delete"),
]


