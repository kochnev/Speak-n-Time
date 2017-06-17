from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    #url(r'^profiles/$', views.list_profiles, name='list_profiles'),
    url(r'^profiles/$', login_required(views.UserProfileListView.as_view()), name='list_profiles'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),

]
