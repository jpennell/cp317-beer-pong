from django import forms
from User.models import *

class LeaderboardForm(forms.Form):
    
    #creates a list of institutions, including 'Overall' option for leaderboard 'choice dropdown'
    choices = ["Overall"]
    queryset = Institution.objects.order_by('_name')
    for x in queryset:
        choices.append(x.getName)

    leaders = [None,None,None,None,None,None,None,None,None,None]