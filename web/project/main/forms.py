from django import forms
from .models import UserProfile
import pytz

class TimeZoneForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('timezone',)




