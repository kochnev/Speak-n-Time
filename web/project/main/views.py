from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.forms import inlineformset_factory

from myregistration.forms import UserProfileForm, CustomInlineFormset
from .forms import TimeZoneForm
from .models import UserProfile, UserLanguage, Language 

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
    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    user_languages = UserLanguage.objects.filter(user_profile=user_profile)
    
    UserLanguageInlineFormSet = inlineformset_factory(UserProfile,
                                                      UserLanguage,
                                                      fields=('language','level'),
                                                      formset=CustomInlineFormset,
                                                      extra=1, can_delete=True)

    if request.method == 'POST':

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        formset = UserLanguageInlineFormSet(request.POST, request.FILES, instance=user_profile)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('profile', user.username)
    else:
        form = UserProfileForm(instance=user_profile)
        formset = UserLanguageInlineFormSet(instance=user_profile)
    return render(request,
                  'main/profile.html',
                  {
                      'userprofile': user_profile,
                      'formset': formset,
                      'selecteduser': user,
                      'form': form
                  }
                 )



@login_required
def update_timezone(request):
    user = request.user
    user_profile = user.profile

    if request.method == 'POST':

        form = TimeZoneForm(request.POST, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect('list_profiles')
    else:
        form = TimeZoneForm(instance=user_profile)
    return render(request,
                  'main/user_list.html',
                  {
                      'form': form,
                      'userprofile_list': UserProfile
                  }
                  )

@login_required
def delete_profile(request, username):
    user = User.objects.filter(username=username)
    userprofile = UserProfile.objects.filter(user=user)

    user.delete()
    userprofile.delete()

    return redirect('list_profiles')


