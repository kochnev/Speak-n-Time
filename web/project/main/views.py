from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.forms import inlineformset_factory

from myregistration.forms import UserProfileForm, CustomInlineFormset
from schedule.models import WeeklySchedule
from schedule.utils import get_localize_schedule

from helper.utils import pivot_schedule

from .forms import TimeZoneForm
from .models import UserProfile, UserLanguage, Language 


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


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    user_languages = UserLanguage.objects.filter(user_profile=user_profile)
    
    user_language_inline_form_set = inlineformset_factory(UserProfile,
                                                      UserLanguage,
                                                      fields=('language','level'),
                                                      formset=CustomInlineFormset,
                                                      extra=1, can_delete=True)

    user_schedule_inline_form_set = inlineformset_factory(UserProfile,
                                                      WeeklySchedule,
                                                      fields=('day_of_week', 'time_from', 'time_to'),
                                                      extra=1, can_delete=True)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        lan_formset = user_language_inline_form_set(request.POST, instance=user_profile)
        sched_formset = user_schedule_inline_form_set(request.POST, instance=user_profile)

        if form.is_valid() and lan_formset.is_valid() and sched_formset.is_valid():
            form.save()
            lan_formset.save()
            sched_formset.save()
            return redirect('profile', user.username)
    else:
        form = UserProfileForm(instance=user_profile)
        lan_formset = user_language_inline_form_set(instance=user_profile)
        sched_formset = user_schedule_inline_form_set(instance=user_profile)

    return render(request,
                  'main/edit_profile.html',
                  {
                      'userprofile': user_profile,
                      'lan_formset': lan_formset,
                      'sched_formset': sched_formset,
                      'selecteduser': user,
                      'form': form
                  }
                 )


@login_required
def profile(request, username):
    selected_user = get_object_or_404(User, username=username)

    sel_user_profile = UserProfile.objects.get_or_create(user=selected_user)[0]
    sel_languages = UserLanguage.objects.filter(user_profile=sel_user_profile)
    sel_weekly_schedule = WeeklySchedule.objects.filter(user_profile=sel_user_profile)

    user = request.user
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    weekly_schedule = WeeklySchedule.objects.filter(user_profile=user_profile)

    if selected_user == user:
        sel_user_schedule = sel_weekly_schedule.values_list('day_of_week', 'time_from', 'time_to')
        sel_user_rows = pivot_schedule(sel_user_schedule)

        user_rows = ()
    else:
        sel_user_schedule = get_localize_schedule(sel_user_profile)
        sel_user_rows = pivot_schedule(sel_user_schedule)

        user_schedule = weekly_schedule.values_list('day_of_week', 'time_from', 'time_to')
        user_rows = pivot_schedule(user_schedule)

    return render(
                  request,
                  'main/profile.html',
                  {
                      'userprofile': sel_user_profile,
                      'selecteduser': selected_user,
                      'languages': sel_languages,
                      'days_of_week': WeeklySchedule.DAY_OF_WEEK,
                      'sel_user_rows': sel_user_rows,
                      'user_rows': user_rows,
                  }
    )


