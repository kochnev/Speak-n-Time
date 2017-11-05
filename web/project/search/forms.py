from django import forms
from main.models import Language


class SearchForm(forms.Form):
    GENDER = (
        ('m', 'male'),
        ('f', 'female'),
    )

    native_language = forms.ModelChoiceField(required=False, label="Native", queryset=Language.objects.all(),
                                             widget=forms.Select(attrs={'class': 'form-control', 'id': 'native_language'}))

    learning_language = forms.ModelChoiceField(required=False, label="Learning", queryset=Language.objects.all(),
                                               widget=forms.Select(attrs={'class': 'form-control'}))

    gender = forms.ChoiceField(choices=GENDER, required=False, help_text='Choose gender',
                               widget=forms.RadioSelect())

    is_use_intersection = forms.BooleanField(required=False, label="Use schedule's intersection")