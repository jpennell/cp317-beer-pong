from django.shortcuts import render, redirect
#from django.contrib.auth import authenticate , login
from django.core.context_processors import csrf
from django.core.mail import send_mail, BadHeaderError
from User.forms import RegistrationForm
from User.models import PongUser
from Utilities.utilities import *
from loginViews import *
from Statistics.models import Ranking, LifeStats
import re
from django.contrib import messages
from django.template import Context


def registerNewUser(request):
    """
    
    attempts to register a new user
    
    Contributors:
    Quinton Black
    Erin Cramer
    
        
    """
    username = email = ""
    emailState = ""
    usernameState = ""
    if request.POST:        
        form = RegistrationForm(request.POST)       

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            if _usernameTaken(username):
                suggestedUsernames = suggestUsernames(username,5)
                context = Context({'regTitle': 'Register', 'registrationForm': form,'suggestedUsernames':suggestedUsernames})
                return render(request, 'user/index.html',context)   

            password = regGameUser(username, email)      
            user_status = loginUser(username, password, request)

                       
            return redirect_with_params('/login',user_status=user_status,username=username)
        context = Context({'regTitle': 'Register','registrationForm':form})
        return render(request, 'user/index.html',context)   

        
        
    #otherwise you're register through the url and need to be redirected to the index
    form = RegistrationForm()
    context = Context({'regTitle': 'Register','registrationForm':form})
    return  redirect('/index/',context)



def _usernameTaken(username):
    """
    checks to see if a prospective username is taken
    
    Keyword arguments:
    username -- user's username (str) 
    
    Contributors:
    Quinton Black
    Erin Cramer
    
    Output:
    taken -- True if taken, false if not (boolean)
    """
    taken = False
    try:
        user = PongUser.objects.get(username=username)
        taken = True
    except:
        pass
    return taken

def suggestUsernames(username, numSug):
    """
    finds and returns other usernames similar to the one the user wanted
    
    Keyword arguments:
    username -- user's wanted username (str) 
    variable -- description 
    
    Contributors:
    Quinton Black
    Erin Cramer
    
    Output: 
    suggestions -- comma separated string of potential username (str)
        
    """
    suggestions = []
    names = []
    if not username.isalpha():
        #parse username to get back number in username
        number = _parse_username(username)
        #separate text from numbers in user name
        names = username.split(number)
        number = int(number)
    else:
        names.append(username)
        number = 0
    number = number + 1
    while len(suggestions) < numSug:
        if len(names) == 1:
            suggestion = names[0] + str(number) 
        else:
            suggestion = names[0] + str(number) + names[1]
        if not _usernameTaken(suggestion):
            suggestions.append(suggestion)
        number += 1 
        
    return suggestions




def _parse_username(username):
    
    """
    this function takes a username and returns the last set of numbers in the user name
    for example: cram8680 would return 8680, 123test would return 123, friends123cram8680 would return 8680

    Keyword arguments:
    username -- user's username (str) 
    
    Contributors:
    Erin Cramer
    
    Output:
    username_number - set of numbers from username (int)
    """

    i = 0
    last = len(username)
    while i < len(username):

        if username[i].isdigit():
            
            first = i
            for j in range(i+1, len(username)):
                
                if not username[j].isdigit():
                    
                    last = j
                    i = j
                    break
                
                elif j == len(username)-1:
                    last = j + 1
                    i = j
                    break
                
        i += 1      
        
                    
    username_number = username[first:last]

    return username_number


def regGameUser(username, email):
    """Registers a user and creates all the necessary models

    Keyword arguments:
    username -- user's username (String)
    email -- user's email (String)
    
    
    Contributors:
    Quinton Black
    Matt Hengeveld
    
    Output:
    password - the users new temporary password (String)
    """
    
    password = generatePassword()
    message = """
    
    Hey {},
    
    Here is your temporary password:{}
    
    Time to login and start playing.
    
    Cheers,
    The Pong Tracker Team""".format(username, password)
    
    sendEmail(username, email, password,message)
    user = PongUser.objects.create_user(username=username, email=email, password=password)
    Ranking.objects.create(_user=user)
    LifeStats.objects.create(_user=user)
    
    return password
