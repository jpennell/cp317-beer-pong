from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.template import RequestContext

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

    Output:

    """
    username = password = ''

    if request.POST:
        username = request.POST.get( 'username' )
        password = request.POST.get( 'password' )

        userState = loginUser( username, password, request )

        if userState == SUCCESS:
            return redirect( '/profile/' )
        elif userState == INCORRECT:
            state = "Incorrect Email/Password Combination"
            return render( request, 'user/index.html', {'state':state, 'username': username} )
        else:
            state = "You are currently banned or inactive, please bring a case of beer to the admin to have your account unbanned "
            return  render( request, 'user/banned.html', {'username':username, 'state':state} )

    return  render( request, 'user/index.html' )


def loginUser( username, password, request ):
    """{{Description}}

    Keyword arguments:
    variable -- description
    variable -- description

    Contributors:
    Quinton Black

    Output:

    """
    user = authenticate( username = username, password = password )
    if user is not None:
        if user.is_active and not user.is_banned:
            login( request, user )
            request.session['username'] = username
            return SUCCESS
        return BANNED
    else:
        return INCORRECT





