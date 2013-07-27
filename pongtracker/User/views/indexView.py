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

    
    
    
    username = request.GET.get('username','')
    email = request.GET.get('email','')   
    usernameState = request.GET.get('usernameState','')
    emailState = request.GET.get('emailState','')
    suggestedUsernames = request.GET.get('suggestedUsernames','')
    state =request.GET.get('state','')
    
    
    if  'registration' in request.GET:
        if request.GET['registration']=='invalid':
            print("invalid")
            registrationForm = RegistrationForm(request.POST)
            context = Context({'regTitle': 'Register', 'registrationForm': registrationForm, 'username':username, 'email':email})  
            return render(request, 'user/index.html',context)

    registrationForm = RegistrationForm()
    
    
    
    
    context = Context({'regTitle': 'Register', 'registrationForm': registrationForm, 'username':username, 'email':email})  
    return render(request, 'user/index.html',context)
    
    
 