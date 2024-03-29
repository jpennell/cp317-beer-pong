from django.shortcuts import redirect
from django.contrib.auth import authenticate,  logout
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.template import RequestContext
from django.conf import settings


def logoutUser(request):
    """Handle logout request

    Keyword arguments:
    request -- the logout request
    
    Contributors:
    Quinton Black
    Erin Cramer
    
    Output:
        HTTP response
        
    """
    state = "You have been logged out successfully"    
    try:
        del request.session['username']
        logout(request)
    except KeyError:
        pass
    
    return redirect(settings.SITE_URL+'index',state=state)