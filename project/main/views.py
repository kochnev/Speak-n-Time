from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from main.forms import UserProfileForm
from main.models import UserProfile
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
         'num_visits':num_visits,
        },
    )


class UserProfileListView(generic.ListView):
    model = UserProfile
    paginate_by = 2

'''@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()

    return render(request, 'main/list_profiles.html',
        {'userprofile_list' : userprofile_list})
        '''

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
               {'website': userprofile.website,
               'picture': userprofile.picture}
               )

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
    return render(request,
                  'main/profile.html',
                  {'userprofile': userprofile,
                  'selecteduser': user,
                  'form': form}
                 )

@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form':form}

    return render(request, 'main/registration_profile.html', context_dict)
