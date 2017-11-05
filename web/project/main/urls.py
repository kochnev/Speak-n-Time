from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^profiles/$', views.list_profiles, name='list_profiles'),
    #url(r'^profiles/$', login_required(views.UserProfileListView.as_view()), name='list_profiles'),
    url(r'^edit_profile/(?P<username>[\w\-]+)/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    #url(r'^select2/', include('django_select2.urls')),

]
