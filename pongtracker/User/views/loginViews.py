from django.shortcuts import render, redirect
#from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.template import RequestContext
from User.models import PongUser
from Utilities.utilities import *
from django.contrib import messages

SUCCESS = 'success'
INCORRECT = 'incorrect'
BANNED = 'banned'

def loginUserRequest( request ):
    """

    Contributors:
    Quinton Black
    Erin Cramer


    """
   #a login request has been made therefore must authenticate
    if request.POST:
        username = request.POST.get( 'username' )
        password = request.POST.get( 'password' )
        userState = loginUser( username, password, request )
    #potentially a redirect, or someone hit the url directly
    #if it can't get the username or password from the redirect parameter, then it was hit by the url, and they should be empty strings
    #if it was hit by a redirect (registration page)
    else:
        userState = request.GET.get('user_status','')
        username =  request.GET.get('username','')      
        
       
    #as long as username is not empty strings, we will attempt a login
    if username !='':
        if userState == INCORRECT:
            return redirect_with_params('/index/', username=username)
        
        user = PongUser.objects.get(username=username)
        #if it was successful and it isn't their first login attempt, got to the login page
        if userState == SUCCESS and user.getHasUpdatedProfile():
            return redirect('/profile/')
        
        #it was successful and the user has never logged in before, set the login status to true, and force them to edit their profile
        elif userState == SUCCESS and not user.getHasUpdatedProfile():
            return redirect( '/profile/edit' )
        
        else:
            return  redirect_with_params('/banned/', username=username)

    return  redirect('/index/')

def loginUser(username, password, request):
    
    """{{Description}}

    Keyword arguments:
    username -- user's username
    password -- user's password
    request -- current page request

    Contributors:
    Quinton Black
    Erin Cramer

    Output:
    SUCCESS if login was successful, BANNED if the user has been banned, and INCORRECT if the credentials are wrong
    """
    
    user = authenticate( username = username, password = password )
    if user is not None:
        if user.getIsActive() and not user.getIsBanned():
            login( request, user )
            request.session['username'] = username
            return SUCCESS
        messages.add_message(request,messages.WARNING,"You are currently banned or inactive, please bring a case of beer to the admin to have your account unbanned.")
        return BANNED
    else:
        messages.add_message(request,messages.WARNING,"Incorrect Email/Password Combination, sober up a bit then try again")
        return INCORRECT 