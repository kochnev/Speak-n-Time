from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from myregistration.forms import UserProfileForm
from .models import UserProfile, UserLanguage

# Create your views here.


def index(request):
    """View function for home page of site"""

    num_users=User.objects.all().count()

    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'main/index.html',
        {
         'num_users':num_users,
         'num_visits':num_visits+1,
        },
    )


class UserProfileListView(generic.ListView):
    model = UserProfile
   # paginate_by = 2
    template_name = 'main/user_list.html'

'''
@login_required
def list_profiles(request):
    userprofile_list = User.objects.all()

    return render(request, 'main/userprofile_list.html',
        {'userprofile_list' : userprofile_list})
    
'''


@login_required
def profile(request, username):
    
    user=get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get_or_create(user=user)[0]

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()

            for lan in form.cleaned_data['languages'].all():
                UserLanguage.objects.create(language=lan, user_profile=user_profile, level='A1')

            form.save_m2m()

            return redirect('profile', user.username)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request,
                  'main/profile.html',
                  {
                      'userprofile': user_profile,
                      'selecteduser': user,
                      'form': form
                  }
                 )

@login_required
def delete_profile(request, username):
    user = User.objects.filter(username=username)
    userprofile = UserProfile.objects.filter(user=user)

    user.delete()
    userprofile.delete()

    return redirect('list_profiles')


