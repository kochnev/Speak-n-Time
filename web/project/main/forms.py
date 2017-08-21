from django import forms
from .models import UserProfile
import pytz

class TimeZoneForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('timezone',)

class SearchLanguagePartner(forms.Form):
    GENDER = (
        ('m', 'male'),
        ('f', 'female'),
    )
    pass
    #gender = forms.CharField(max_length=1, default='m', choices=GENDER, help_text='Choose your gender')


