from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from User.models import Profile, Institution

def loginUser(request):
    state = "Please log in below..."
    username = password = ''
    
    if request.POST:
        username=request.Post.get('username')
        password=request.Post.get('password')
        
        user = authenticate(username=username,password=password)
        if user is not None:
            #check for banned
            if user.is_active:
                login(request,user)
                state = "You're successfully logged in!"
            else:
                state= "Your account is not active, please contact the site administrator"
        else:
            state = "Your username and/or password were incorrect."
    return  render_to_response('main.html')