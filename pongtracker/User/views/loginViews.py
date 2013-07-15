from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.template import RequestContext

SUCCESS = 0
INCORRECT = 1
BANNED = 2 

def loginUserRequest(request):
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
        username=request.POST.get('username')
        password=request.POST.get('password')
           
        userState = loginUser(username,password,request)
        
        if userState==SUCCESS:
            return  render_to_response('user/profile.html',{'username': username},context_instance=RequestContext(request))
        elif userState == INCORRECT:
            state = "Incorrect Email/Password Combination"
            return render_to_response('user/login.html',{'state':state, 'username': username},context_instance=RequestContext(request))
        else:
            return  render_to_response('user/banned.html',{'username':username},context_instance=RequestContext(request))
    
    return  render_to_response('user/index.html',context_instance=RequestContext(request))


def loginUser(username,password,request):    
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    
    Output:
        
    """
    user = authenticate(username=username,password=password)   
    if user is not None:                                   
        if user.is_active and not user.get_profile().is_banned:
            login(request,user)
            request.session['username']=username
            return SUCCESS
        return BANNED
    else:         
        return INCORRECT


    
    
    
