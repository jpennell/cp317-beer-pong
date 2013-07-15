from django.shortcuts import render_to_response
from django.contrib.auth import authenticate,  logout
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.template import RequestContext



def logoutUser(request):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    
    Output:
        
    """
    state = "You have been logged out successfully"
    try:
        del request.session['username']
        logout(request)
    except KeyError:
        pass
    
    return render_to_response('user/index.html',{'state':state, 'username': ""},context_instance=RequestContext(request))