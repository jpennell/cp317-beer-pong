from django import forms
from User.models import *

class LeaderboardForm(forms.Form):
    """Creates a list of institutions, including 'Overall' option for leaderboard 'choice dropdown'

    Keyword arguments:
    form -- a django form object
    
    Contributors:
    Richard Douglas

    """
   
    choices = ["Overall"]
    queryset = Institution.objects.order_by('_name')
    for x in queryset:
        choices.append(x.getName)

    leaders = [None,None,None,None,None,None,None,None,None,None]