from django import forms
import datetime
from User.models import Institution

class EditProfileForm(forms.Form):
    year_choices = []
    for r in range((datetime.datetime.now().year),(datetime.datetime.now().year+10)):
        year_choices.append((r,r))
        
    year_tuple = (year_choices)
        
    firstname = forms.CharField(max_length=250)
    lastname = forms.CharField(max_length=250)
    email = forms.EmailField(max_length=250)
    height = forms.IntegerField(max)
    photo = forms.ImageField()
    #graduation_year = forms.ChoiceField(('year'), max_length=4, choices=year_tuple)
    #institution = forms.ModelChoiceField(Institution.all())
    