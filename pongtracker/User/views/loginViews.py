from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.template import RequestContext
from User.models import PongUser
from Utilities.utilities import *

SUCCESS = 0
INCORRECT = 1
BANNED = 2

def loginUserRequest( request ):
    """{{Description}}

    Keyword arguments:
    variable -- description
    variable -- description

    Contributors:
    Quinton Black
    Erin Cramer

    Output:

    """
    #a login request has been made
    if request.POST:
        username = request.POST.get( 'username' )
        password = request.POST.get( 'password' )
        user = _authenticate(username, password)
    #potentially a redirect, or someone hit the url directly
    #if it can't get the username or password from the redirect parameter, then it was hit by the url, and they should be empty strings
    else:
        state = request.GET.get('state','')
        username = request.GET.get('username','')            
        
    if state:

        return render(request, 'user/login.html', {'state':state, 'username':username})
    
    #as long as username and password are not empty strings, we will attempt a login
    elif username != '':
        
        user = PongUser.objects.get(username=username)
        userState = _loginUser( username, password, request )
        
        #if it was successful and it isn't their first login attempt, got to the login page
        if userState == SUCCESS and user.getHasLoggedIn():
            return redirect('/profile/')
        
        #it was successful and the user has never logged in before, set the login status to true, and force them to edit their profile
        elif userState == SUCCESS and not user.getHasLoggedIn():
            return redirect( '/profile/edit' )
        
        elif userState == INCORRECT:
            state = "Incorrect Email/Password Combination"
            return redirect_with_params('/login/', username=username, state=state)
        
        else:
            state = "You are currently banned or inactive, please bring a case of beer to the admin to have your account unbanned."
            return  redirect_with_params('/banned/', username=username, state=state)

    return  redirect('/index/')


def _authenticate( username, password ):
    """{{Description}}

    Keyword arguments:
    variable -- description
    variable -- description

    Contributors:
    Quinton Black
    Erin Cramer

    Output:

    """
    user = authenticate( username = username, password = password )
    return user


def _loginUser(user, request):
    
    """{{Description}}

    Keyword arguments:
    variable -- description
    variable -- description

    Contributors:
    Quinton Black
    Erin Cramer

    Output:

    """

    if user is not None:
        if user.getIsActive() and not user.getIsBanned():
            login( request, user )
            request.session['username'] = username
            return SUCCESS
        return BANNED
    else:
        return INCORRECT 