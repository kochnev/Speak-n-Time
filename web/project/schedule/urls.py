from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^myschedule/(?P<username>[\w\-]+)/$', views.my_schedule, name='my_schedule'),
]
