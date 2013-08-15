from django.shortcuts import render
from User.forms import RegistrationForm
from django.template import Context
from Statistics.forms.leaderboardForm import LeaderboardForm
from Statistics.views.leaderBoardView import *

def viewHomepageRequest(request):
    """Renders the registration page 

    Keyword arguments:
    the request for the homepage
    
    Contributors:
    Erin Cramer
    Quinton Black
    Matthew Hengeveld
    
    Output:
        HTTP response
        
    """ 
    leaderForm = LeaderboardForm()
    
    topRanked = getTopRanked(10)
    displayBoard(topRanked, leaderForm)
    
    registrationForm = RegistrationForm()

    context = Context({'regTitle': 'Register', 'registrationForm': registrationForm, 'leaderForm': leaderForm})  
    return render(request, 'user/index.html',context)
    
    
 