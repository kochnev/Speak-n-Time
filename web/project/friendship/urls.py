from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^friends/(?P<username>[\w-]+)/$', views.friendship_view_friends, name='friendship_view_friends'),
    url(r'^friend/add/(?P<to_username>[\w-]+)/$', views.friendship_create_request, name='friendship_create_request'),
    url(r'^friend/requests/$', views.friendship_request_list, name='friendship_request_list'),
    url(
        regex=r'^friend/request/(?P<friendship_request_id>\d+)/$',
        view=views.friendship_request_detail,
        name='friendship_request_detail',
    ),
    url(
        regex=r'^friend/accept/(?P<friendship_request_id>\d+)/$',
        view=views.friendship_accept,
        name='friendship_accept',
    ),
    url(
        regex=r'^friend/reject/(?P<friendship_request_id>\d+)/$',
        view=views.friendship_reject,
        name='friendship_reject',
    ),
    url(
        regex=r'^friend/cancel/(?P<friendship_request_id>\d+)/(?P<to_username>[\w-]+)/$',
        view=views.friendship_cancel,
        name='friendship_cancel',
    ),
]

