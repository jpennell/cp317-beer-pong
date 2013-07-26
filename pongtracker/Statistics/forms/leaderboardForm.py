from django import forms
from User.models import *

class LeaderboardForm(forms.Form):
    
    _choices = ["Overall"]
    queryset = Institution.objects.all()
    for x in queryset:
        _choices.append(x)
    
#     institution = forms.ModelChoiceField( 
#         choices = _choices,
#         required = True,
#         label = "View"
#     )
    
    leaders = [None,None,None,None,None,None,None,None,None,None]