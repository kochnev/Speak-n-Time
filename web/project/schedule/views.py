from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from main.models import UserProfile
from .models import WeeklySchedule

from helper.utils import pivot_schedule


def my_schedule(request,username):
    """For editing and rendering weekly schedule"""

    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    weekly_schedule = WeeklySchedule.objects.filter(user_profile=user_profile)

    userScheduleInlineFormSet = inlineformset_factory(UserProfile, WeeklySchedule,
                                                      fields=('day_of_week', 'time_from', 'time_to'),
                                                      extra=1, can_delete=True)

    # prepare data for rendering in table
    user_schedule = weekly_schedule.values_list('day_of_week','time_from','time_to')
    rows = pivot_schedule(user_schedule)

    if request.method == 'POST':
        formset = userScheduleInlineFormSet(request.POST, instance=user_profile,)
        if formset.is_valid():
            formset.save()
            return redirect('my_schedule', user.username)
    else:
        formset = userScheduleInlineFormSet(instance=user_profile,)

    return render(
        request,
        'schedule/myschedule.html',
        {
            'formset': formset,
            'days_of_week': WeeklySchedule.DAY_OF_WEEK,
            'data': rows,
        }
    )


