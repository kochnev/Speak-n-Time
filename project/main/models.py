from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    """Model reprsenting a language (e.g Engilsh, Russian)"""

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

    languages = models.ManyToManyField(
        Language,
        through='UserLanguage',
        related_name='native_language',
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

class UserLanguage(models.Model):
    """Model representing a ling between user and language"""
    user_profile = models.ForeignKey(UserProfile)
    language = models.ForeignKey(Language)
    native = models.BooleanField(default=False)

    LEVEL = (
        ('A1', 'Beginner'),
        ('A2', 'Elementary'),
        ('B1', 'Intermediate'),
        ('B2', 'Upper intermediate'),
        ('C1', 'Advanced'),
        ('C2', 'Proficient'),
    )

    level = models.CharField(max_length=2, choices=LEVEL, help_text='Choose your level', blank=True)

    def __str__(self):
        """String for representing the Model object"""
        return self.user_profile.user.username + ' ' + self.language.name
