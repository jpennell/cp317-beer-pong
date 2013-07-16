from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from User.models import Institution
from django.core.context_processors import csrf
from django.template import RequestContext



def viewProfile(request):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    
    Output:
        
    """
    if 'username' in request.session:
        username = request.session['username']
        return render_to_response('user/profile.html',{'username': username},context_instance=RequestContext(request))
    else:
        return  render_to_response('user/index.html',context_instance=RequestContext(request))