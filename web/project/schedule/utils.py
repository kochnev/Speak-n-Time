import pytz
import datetime

from django.utils import timezone

from .models import WeeklySchedule


def get_localize_schedule(user_profile):
    """ function takes user's schedule and transform it into localtime """
    #import pdb; pdb.set_trace()
    user_tz = user_profile.timezone
    weekly_schedule = WeeklySchedule.objects.filter(user_profile=user_profile)
    user_schedule = weekly_schedule.values('day_of_week', 'time_from', 'time_to')

    my_schedule = tuple()
    zero_time = datetime.time(0,0,0)
    for item in user_schedule:
        day_of_week = item['day_of_week']
        time_from = item['time_from']
        time_to = item['time_to']

        my_time_from, day_of_week_from = get_localize_time(time_from, day_of_week, user_tz)
        my_time_to, day_of_week_to = get_localize_time(time_to,day_of_week, user_tz)

        if day_of_week_from != day_of_week_to:
            my_schedule = my_schedule + ((day_of_week_from, my_time_from, zero_time),)
            if my_time_to != zero_time:
                my_schedule = my_schedule + ((day_of_week, zero_time, my_time_to),)
        else:
            my_schedule = my_schedule + ((day_of_week, my_time_from, my_time_to),)

    return my_schedule


def get_localize_time(time, day_of_week, user_tz):
    """function to transform naive time into local time"""

    days = [d[0] for d in WeeklySchedule.DAY_OF_WEEK]
    day_index = days.index(day_of_week)

    d = datetime.datetime.today()
    dt_naive = datetime.datetime.combine(d, time)
    dt_aware = timezone.make_aware(dt_naive, pytz.timezone(user_tz))
    my_dt_aware = timezone.localtime(dt_aware)

    if my_dt_aware.date() < dt_aware.date():
        day_index -= 1
    elif my_dt_aware.date() > dt_aware.date():
        day_index += 1
        if day_index >= 7:
            day_index = day_index - 7

    day_of_week = days[day_index]

    return my_dt_aware.time(), day_of_week





