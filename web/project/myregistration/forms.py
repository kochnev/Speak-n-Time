import datetime
from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    current_date = datetime.datetime.now()
    years_to_display = range(current_date.year - 100, current_date.year)
                             
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=years_to_display),
                    initial=current_date)
    class Meta:
        model = UserProfile
        exclude = ('user', )
