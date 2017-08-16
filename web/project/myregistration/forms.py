from django.utils import timezone
from django import forms
from django.forms import BaseInlineFormSet
from django.contrib.auth.models import User
from main.models import UserProfile


class CustomInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CustomInlineFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['language'].widget.attrs['class'] = 'form-control'
            form.fields['level'].widget.attrs['class'] = 'form-control'



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    current_date = timezone.now()
    years_to_display = range(current_date.year - 100, current_date.year)
                             
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(attrs=({'style': 'width: 33%; display: inline-block;'})))
    #forms.DateField(widget=forms.SelectDateWidget(years=years_to_display),
     #    initial=current_date)

    class Meta:
        model = UserProfile
        fields = ('picture', 'timezone', 'last_login', 'website', 'birthday', 'gender' )

    def __init__(self, *args, **kwargs):
        form = super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



