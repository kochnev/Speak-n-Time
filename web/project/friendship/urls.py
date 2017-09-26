from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(
        regex=r'^friends/(?P<username>[\w-]+)/$',
        view=views.friendship_friends_list,
        name='friendship_friends_list'
    ),
    url(
        regex=r'^friend/add/(?P<to_username>[\w-]+)/$',
        view=views.friendship_create_request,
        name='friendship_create_request'
    ),
    url(
        regex=r'^friend/remove/(?P<to_username>[\w-]+)/$',
        view=views.friendship_remove,
        name='friendship_remove',
    ),
    url(
        regex=r'^friend/request/accept/(?P<friendship_request_id>\d+)/$',
        view=views.friendship_accept,
        name='friendship_accept',
    ),
    url(
        regex=r'^friend/request/reject/(?P<friendship_request_id>\d+)/$',
        view=views.friendship_reject,
        name='friendship_reject',
    ),
    url(
        regex=r'^friend/request/cancel/(?P<friendship_request_id>\d+)/(?P<to_username>[\w-]+)/$',
        view=views.friendship_cancel,
        name='friendship_cancel',
    ),
]

