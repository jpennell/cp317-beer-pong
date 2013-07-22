from django.shortcuts import render, redirect

def viewHomepage(request):
    """
    {{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Erin Cramer
    
    Output:
        
    """ 
    print("Viewing Homepage")
    
    username = request.GET.get('username','')
    email = request.GET.get('email','')   
    usernameState = request.GET.get('usernameState','')
    emailState = request.GET.get('emailState','')
    suggestedUsernames = request.GET.get('suggestedUsernames','')
    state =request.GET.get('state','')
    
    if suggestedUsernames:
        suggestedNames = suggestedUsernames.split(",")
        return render(request, 'user/index.html', {'username':username, 'email':email, 'usernameState':usernameState, 'suggestedUsernames':suggestedNames})
    elif usernameState:
        return render(request, 'user/index.html', {'username':username, 'email':email, 'usernameState':usernameState})
    elif emailState:
        return render(request, 'user/index.html', {'username':username, 'email':email, 'emailState':emailState})
    elif state:
        return render(request, 'user/index.html', {'state':state})
    else:   
        return render(request, 'user/index.html')