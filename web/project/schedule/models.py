from django.db import models
from main.models import UserProfile
from django.utils import timezone


# Create your models here.

class WeeklySchedule(models.Model):
    """Model representing a weekly schedule of user"""

    user_profile = models.ForeignKey(UserProfile)

    DAY_OF_WEEK =(
        (1,'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK)

    time_from = models.TimeField()
    time_to = models.TimeField()


    #def save(self, *args, **kwargs):
    #    #do something
    #    self.dt_from = timezone.now().replace()
    #    super(WeeklySchedule, self).save(*args, * kwargs)


