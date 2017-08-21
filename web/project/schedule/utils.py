import pytz
import datetime

from django.utils import timezone

from .models import WeeklySchedule


def get_localize_schedule(user_profile):
    """ function takes user's schedule and transform it into localtime """
    user_tz = user_profile.timezone
    weekly_schedule = WeeklySchedule.objects.filter(user_profile=user_profile)
    user_schedule = weekly_schedule.values_list('day_of_week', 'time_from', 'time_to')

    for item in user_schedule:
        day_of_week = item['day_of_week']
        time_from = item['time_from']
        time_to = item['time_to']

        d = datetime.datetime.today()

        dt_naive = datetime.datetime.combine(d, time_from)

        dt_aware = timezone.make_aware(dt_naive, pytz.timezone(user_tz))

       # my_dt_aware =


