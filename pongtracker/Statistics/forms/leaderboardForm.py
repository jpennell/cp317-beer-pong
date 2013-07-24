from django import forms
from User.models import *

class LeaderboardForm(forms.Form):
    
    _choices = ["Overall"]
    _choices.append(Institution.objects.all())
    
    institution = forms.ModelChoiceField( 
        queryset=_choices,
        required = True,
        label = "View"
    )