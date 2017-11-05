from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

import pytz



class TimeZoneForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('timezone',)




