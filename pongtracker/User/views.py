from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from User.models import Profile, Institution
from django.core.context_processors import csrf
from django.template import RequestContext

def loginUser(request):

    state = ""
    username = password = ''
    
    if request.POST:
        usernameRequest=request.POST.get('username')
        passwordRequest=request.POST.get('password')
           
        user = authenticate(username=usernameRequest,password=passwordRequest)

        if user is not None:
            #check for banned
            if user.is_active:
                login(request,user)
                request.session['username']=usernameRequest
                return  render_to_response('user/profile.html',{'username': usernameRequest},context_instance=RequestContext(request))

            else:
                state= "Your account is not active, please contact the site administrator"
        else:
            state = "Your username and/or password were incorrect."
            return  render_to_response('user/index.html',{'state':state, 'username': usernameRequest},context_instance=RequestContext(request))
            
    
    return  render_to_response('user/index.html',{'state':state, 'username': ""},context_instance=RequestContext(request))


def logoutUser(request):
    state = "You have been logged out successfully"
    try:
        del request.session['username']
        logout(request)
    except KeyError:
        pass
    
    return render_to_response('user/index.html',{'state':state, 'username': ""},context_instance=RequestContext(request))


def viewProfile(request):
    if 'username' in request.session:
        username = request.session['username']
        return render_to_response('user/profile.html',{'username': username},context_instance=RequestContext(request))
    else:
        return  render_to_response('user/index.html',context_instance=RequestContext(request))
    
    
