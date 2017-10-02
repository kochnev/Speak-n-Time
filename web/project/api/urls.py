from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        regex=r'^get_users/$',
        view=views.get_users,
        name='get_users'
    ),

]

