from django.shortcuts import render, redirect
from User.forms import RegistrationForm
from django.template import Context
from Statistics.forms.leaderboardForm import LeaderboardForm
from Statistics.views.leaderBoardView import *

def viewHomepageRequest(request):
    """
    {{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Erin Cramer
    Quinton Black
    Matthew Hengeveld
    
    Output:
        
    """ 
    leaderForm = LeaderboardForm()
    
    topRanked = getTopRanked(10)
    displayBoard(topRanked, leaderForm)
    
    registrationForm = RegistrationForm()

    context = Context({'regTitle': 'Register', 'registrationForm': registrationForm, 'leaderForm': leaderForm})  
    return render(request, 'user/index.html',context)
    
    
 