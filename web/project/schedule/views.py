from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from main.models import UserProfile
from .models import WeeklySchedule
# Create your views here.

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
    user_schedule_dict = defaultdict(list)

    #example dict data: {'Mo':[(time_from1, time_to1),(time_from2, time_to2)], 'Fr':[(time_from3, time_to3)]}
    for item in user_schedule:
        user_schedule_dict[item[0]].append((item[1], item[2]),)

    days_of_week = [day[0] for day in WeeklySchedule.DAY_OF_WEEK]

    # example columns: [[(time_from1,time_to2)],[],[],[(time_from3,time_from3),(time_from4,time_to4)],[],[],[]]
    columns = [user_schedule_dict[day] for day in days_of_week]

    # get the length of the longest column
    max_len = len(max(columns, key=len))

    for col in columns:
        # padding the short columns with None
        col += [None,] * (max_len - len(col))

    # Then rotate the structure...
    rows=[[col[i] for col in columns] for i in range(max_len)]

    if request.method == 'POST':
        formset = userScheduleInlineFormSet(request.POST, instance=user_profile)
        if formset.is_valid():
            formset.save()
            return redirect('my_schedule', user.username)
    else:
        formset = userScheduleInlineFormSet(instance=user_profile)

    return render(
        request,
        'schedule/myschedule.html',
        {
            'formset': formset,
            'weekly_schedule': weekly_schedule,
            'days_of_week': WeeklySchedule.DAY_OF_WEEK,
            'data': rows,
        }
    )


