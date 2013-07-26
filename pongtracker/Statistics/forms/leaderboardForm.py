from django import forms
from User.models import *

class LeaderboardForm(forms.Form):
    
    choices = ["Overall"]
    queryset = Institution.objects.order_by('_name')
    for x in queryset:
        choices.append(x.getName)
    
#     institution = forms.ModelChoiceField( 
#         choices = _choices,
#         required = True,
#         label = "View"
#     )
    
    leaders = [None,None,None,None,None,None,None,None,None,None]