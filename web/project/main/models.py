from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

LEVEL = (
    ('A1', 'Beginner'),
    ('A2', 'Elementary'),
    ('B1', 'Intermediate'),
    ('B2', 'Upper intermediate'),
    ('C1', 'Advanced'),
    ('C2', 'Proficient'),
    ('N', 'Native'),
)


class Language(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)

    def __str__(self):
        """ String for representing Language object """
        return self.name


# Create your models here.
class UserProfile(models.Model):
    """Model representing a userprofile (additional info about user) """
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    birthday = models.DateField(blank=True, null=True)

    languages = models.ManyToManyField(
        Language,
        through='UserLanguage',
        help_text='Input language(e.g. english, russian, ukranian)')

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

    #def display_language(self):
    #    """Creates a string for the list of language."""
    #    return ', '.join([ lang.name for lang in self.language.all()[:3]])

class UserLanguage(models.Model):
    """Model representing a link between user and language"""
    user_profile = models.ForeignKey(UserProfile)
    language = models.ForeignKey(Language)

    level = models.CharField(max_length=2, choices=LEVEL, help_text='Choose your level')

    def __str__(self):
        """String for representing the Model object"""
        return self.user_profile.user.username + ' ' + self.language.name

    #class Meta():
    #    auto_created = True

