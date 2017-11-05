from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        regex=r'^get_users/$',
        view=views.get_users,
        name='get_users'
    ),
url(
        regex=r'^get_languages/$',
        view=views.get_languages,
        name='get_languages'
    ),

]

