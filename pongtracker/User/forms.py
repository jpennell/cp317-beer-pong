from django import forms
import datetime
from User.models import Institution

class EditProfileForm(forms.Form):
    year_choices = []
    for r in range((datetime.datetime.now().year),(datetime.datetime.now().year+11)):
        year_choices.append((r,r))
        
    year_tuple = (year_choices)
        
    firstname = forms.CharField(max_length=250)
    lastname = forms.CharField(max_length=250)
    email = forms.EmailField(max_length=250)
    height = forms.IntegerField(max)
    institution = forms.ModelChoiceField(Institution.objects.all(),empty_label="No institutions")
    graduation_year = forms.ChoiceField(choices=year_tuple)
    photo = forms.ImageField(label="Profile Photo")
    deactivate = forms.BooleanField(label="I would like to deactivate my account.")