import pytz
import datetime

from django.utils import timezone

from .models import WeeklySchedule


def get_localize_schedule(user_profile):
    """ function takes user's schedule and transform it into localtime """
    user_tz = user_profile.timezone
    weekly_schedule = WeeklySchedule.objects.filter(user_profile=user_profile)
    user_schedule = weekly_schedule.values('day_of_week', 'time_from', 'time_to')

    my_schedule = tuple()

    for item in user_schedule:
        day_of_week = item['day_of_week']
        time_from = item['time_from']
        time_to = item['time_to']

        my_time_from = get_localize_time(time_from, user_tz)
        my_time_to = get_localize_time(time_to, user_tz)

        my_schedule = my_schedule + ((day_of_week, my_time_from, my_time_to),)

    return my_schedule

def get_localize_time(time, user_tz):

    d = datetime.datetime.today()

    dt_naive = datetime.datetime.combine(d, time)

    dt_aware = timezone.make_aware(dt_naive, pytz.timezone(user_tz))

    my_dt_aware = timezone.localtime(dt_aware)

    return my_dt_aware.time()





