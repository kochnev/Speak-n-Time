from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^friend/add/(?P<to_username>[\w-]+)/$', views.friendship_create_request, name='friendship_create_request'),
]
