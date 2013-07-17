from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from User.models import Institution
from django.core.context_processors import csrf
from django.template import RequestContext


def viewProfile( request, username = None ):
    """{{Description}}

    Keyword arguments:
    variable -- description
    variable -- description

    Contributors:
    Quinton Black

    Output:

    """
    print(username)
    
    
    if username == None:
        username = request.session['username']
    return render( request, 'user/profile.html' )
