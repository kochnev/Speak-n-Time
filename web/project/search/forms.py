from django import forms
from main.models import Language

class SearchForm(forms.Form):
    GENDER = (
        ('','-----'),
        ('m', 'male'),
        ('f', 'female'),
    )

    native_language = forms.ModelChoiceField(required=False, label="Native", queryset=Language.objects.all(),
                                             widget=forms.Select(attrs={'class': 'form-control'}))

    learning_language = forms.ModelChoiceField(required=False, label="Learning", queryset=Language.objects.all(),
                                             widget=forms.Select(attrs={'class': 'form-control'}))

    gender = forms.ChoiceField(choices=GENDER, required=False, help_text='Choose gender',
                               widget=forms.Select(attrs={'class': 'form-control'}))

    is_use_intersection = forms.BooleanField(required=False, label="Use schedule's intersection")