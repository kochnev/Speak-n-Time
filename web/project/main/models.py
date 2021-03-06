import pytz
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Language(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)

    def __str__(self):
        """ String for representing Language object """
        return self.name

class Country(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)

    def __str__(self):
        """ String for representing Country object """
        return self.name


# Create your models here.
class UserProfile(models.Model):
    """Model representing a userprofile (additional info about user) """
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, related_name='profile')

    # The additional attributes we wish to include.

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    birthday = models.DateField(blank=True, null=True)
    last_login = models.DateTimeField(default=timezone.now)
    #skypename = models.CharField(max_length=255)
    video_link = models.CharField(max_length=255, blank=True)
    ##is_checked = models.BooleanField(default=False)

    languages = models.ManyToManyField(
        Language,
        through='UserLanguage',
        help_text='Input language(e.g. english, russian, ukranian)')

    timezone = models.CharField(
        max_length=255,
        choices=[(t,t) for t in pytz.common_timezones],
        blank=True, null=True)
    # Override the __inicode__() method to return out something meaningful!

    GENDER = (
        ('m', 'male'),
        ('f', 'female'),
    )

    gender = models.CharField(max_length=1, default='m', choices=GENDER, help_text='Choose your gender')

    def __str__(self):
        """String for representing the Model object"""
        return self.user.username

    def get_absolute_url(self):
        """Returns the url to access a particular user profile"""

        return reverse('profile', args=[str(self.user.username)])

    def get_native_languages(self):
        """Returns list of user's native languages"""
        return self.userlanguage_set.filter(level='N')

    def get_learning_languages(self):
        """Returns list of languages which user are learning"""
        return self.userlanguage_set.exclude(level='N')

    #def display_language(self):
    #    """Creates a string for the list of language."""
    #    return ', '.join([ lang.name for lang in self.language.all()[:3]])

class UserLanguage(models.Model):
    """Model representing a link between user and language"""
    user_profile = models.ForeignKey(UserProfile)
    language = models.ForeignKey(Language)

    LEVEL = (
        ('A1', 'Beginner'),
        ('A2', 'Elementary'),
        ('B1', 'Intermediate'),
        ('B2', 'Upper intermediate'),
        ('C1', 'Advanced'),
        ('C2', 'Proficient'),
        ('N', 'Native'),
    )

    level = models.CharField(max_length=2, choices=LEVEL, help_text='Choose your level')

    def __str__(self):
        """String for representing the Model object"""
        return self.user_profile.user.username + ' ' + self.language.name

    #class Meta():
    #    auto_created = True


#class LanguagePartners(models.Model):
    """Model representing info if two users are language partner"""


