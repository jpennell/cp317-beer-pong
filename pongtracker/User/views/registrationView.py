from django.shortcuts import render, redirect
from django.contrib.auth import authenticate , login
from django.core.context_processors import csrf
from django.core.mail import send_mail
#from User.forms import RegistrationForm
from User.models import PongUser
import random
from Utilities.utilities import *


def registerNewUser(request):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    Erin Cramer
    
    Output:
        
    """
    username = email = ""
    emailState = ""
    usernameState = ""
    if request.POST:
        
#        form = RegistrationForm(request.POST)
#        if form.is_valid():
#            
#            username = form.cleaned_data['username']
#            email = form.cleaned_data['email']
            
        username = request.POST.get('username')
        email = request.POST.get('email')

        if not _validateUsername(username):
            usernameState = 'User name does not fit the format 30 characters or fewer. Letters, digits and @/./+/-/_ only.'
            return  redirect_with_params('/index/', usernameState=usernameState, username=username, email=email)
    
        if _usernameTaken(username):
            usernameSuggestions = _suggestUsernames(username)
            usernameState = 'That user name is taken, here are some suggestions:'
            return redirect_with_params('/index/', usernameState=usernameState, suggestedUsernames=usernameSuggestions, email=email, username=username)
        
        if not _validateEmail(email):
            emailState = "Please provide a valid email address"
            print("Got to validate email function")
            return  redirect_with_params('/index/',emailState=emailState, username=username, email=email)
            
        password = _generatePassword()
        _sendEmail(username, email, password)
        PongUser.objects.create_user(username=username, email=email, password=password)
        
        return redirect_with_params('/login',username=username)
    
    #otherwise you're register through the url and need to be redirected to the index
    return  redirect('/index/')

#Needs to be done better
def _validateEmail(email):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    
    Output:
        
    """
    valid = True
    if email.count('@') != 1:
        valid = False
    if email.count('.') < 1:
        valid = False
    return valid

#Needs to be done better
def _validateUsername(username):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    
    Output:
        
    """
    valid = True
    return valid

def _usernameTaken(username):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
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

def _suggestUsernames(username):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    Erin Cramer
    
    Output: 
    suggestions -- comma separated string (str)
        
    """
    suggestions = []
    names = []
    if not username.isalpha():
        #parse username to get back number in username
        number = _parse_username(username)
        names = username.split(number)
        number = int(number)
    else:
        names.append(username)
        number = 0
    number = number + 1
    while len(suggestions) < 5:
        if len(names) == 1:
            suggestion = names[0] + str(number) 
        else:
            suggestion = names[0] + str(number) + names[1]
        if not _usernameTaken(suggestion):
            suggestions += [suggestion]  
        number += 1 
        
    return ",".join(suggestions)


def _sendEmail(username, email, password):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    
    Output:
        
    """

#    send_mail( 'Pong Tracker Account', "Here is your temporary password:{0}".format( password ),
#               email, ['from@hotmail.com'], fail_silently = False )

    return

def _generatePassword():
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    
    Output:
        
    """
    password = "Bubbles"

    return password

def _parse_username(username):
    
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    
    Output:
        
    """

    i = 0
    while i < len(username):

        if not username[i].isalpha():
            
            first = i
            for j in range(i+1, len(username)):
                
                if username[j].isalpha():
                    
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
