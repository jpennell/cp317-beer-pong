from django import forms
import datetime
from User.models import Institution

class EditProfileForm(forms.Form):
    year_choices = []
    for r in range((datetime.datetime.now().year),(datetime.datetime.now().year+11)):
        year_choices.append((r,r))
        
    year_tuple = (year_choices)
        
    firstname = forms.CharField(label="First Name",max_length=250)
    lastname = forms.CharField(label="Last Name",max_length=250)
    email = forms.EmailField(label="Email",max_length=250)
    height = forms.IntegerField(label="Height")
    institution = forms.ModelChoiceField(Institution.objects.all(),empty_label="No institutions", required=False)
    graduation_year = forms.ChoiceField(choices=year_tuple)
    photo = forms.ImageField(label="Profile Photo", required=False)
    deactivate = forms.BooleanField(label="I would like to deactivate my account.", required=False)