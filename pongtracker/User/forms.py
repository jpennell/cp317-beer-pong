from django import forms
import datetime
from User.models import Institution

class EditProfileForm(forms.Form):
    year_choices = []
    for r in range((datetime.datetime.now().year),(datetime.datetime.now().year+10)):
        year_choices.append((r,r))
        
    firstname = forms.CharField(max_length=250)
    lastname = forms.CharField(max_length=250)
    email = forms.EmailField(max_length=250)
    height = forms.SmallIntegerField(null = True, blank = True)
    photo = forms.CharField(max_length=100, null = True, blank = True)
    graduation_year = forms.IntegerField(('year'), max_length=4, choices=year_choices, default=datetime.datetime.now().year+1)
    institution = forms.ModelChoiceField(Institution.object.all())
    