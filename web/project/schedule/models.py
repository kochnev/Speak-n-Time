from django.db import models
from main.models import UserProfile


# Create your models here.

class WeeklySchedule(models.Model):
    """Model representing a weekly schedule of user"""

    user_profile = models.ForeignKey(UserProfile)

    DAY_OF_WEEK =(
        ('Mo','Monday'),
        ('Tu', 'Tuesday'),
        ('We', 'Wednesday'),
        ('Th', 'Thursday'),
        ('Fr', 'Friday'),
        ('Sa', 'Saturday'),
        ('Su', 'Sunday'),
    )
    day_of_week = models.CharField(max_length=2, choices=DAY_OF_WEEK, )

    time_from = models.TimeField()
    time_to = models.TimeField()

