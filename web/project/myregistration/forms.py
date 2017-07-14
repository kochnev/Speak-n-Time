from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    birthday = forms.DateField(input_formats=['%d/%m/%Y'])
    class Meta:
        model = UserProfile
        exclude = ('user', )
