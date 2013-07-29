from django.shortcuts import render, redirect
from User.forms import RegistrationForm
from django.template import Context
from Statistics.forms.leaderboardForm import LeaderboardForm

def viewHomepage(request):
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
    registrationForm = RegistrationForm()

    context = Context({'regTitle': 'Register', 'registrationForm': registrationForm, 'leaderForm': leaderForm})  
    return render(request, 'user/index.html',context)
    
    
 