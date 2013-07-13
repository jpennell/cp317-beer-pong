from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from User.models import Profile, Institution
from django.core.context_processors import csrf
from django.template import RequestContext

def editProfile(request):
    username = "teemo"
    
    return render_to_response('user/editProfile.html',{'username': username},context_instance=RequestContext(request))
    