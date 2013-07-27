from django.shortcuts import render, redirect
from User.forms import RegistrationForm
from django.template import Context

def viewHomepage(request):
    """
    {{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Erin Cramer
    Quinton Black
    
    Output:
        
    """ 
    registrationForm = RegistrationForm()

    context = Context({'regTitle': 'Register', 'registrationForm': registrationForm})  
    return render(request, 'user/index.html',context)
    
    
 