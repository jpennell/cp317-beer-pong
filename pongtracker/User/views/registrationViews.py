from django.shortcuts import render_to_response
from django.contrib.auth import authenticate , login
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.mail import send_mail
#from User.forms import RegistrationForm
from User.models import PongUser


def registerNewUser(request):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    
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
            return  redirect('/index/', usernameState=usernameState, username=username, email=email)
    
        if _usernameTaken(username):
            usernameSuggestions = _suggestUsernames(username)
            usernameState = 'That user name is taken, here are some suggestions:'
            return redirect('/index/', usernameState=usernameState, suggestedUsername=usernameSuggestions, email=email, username=username)
        
        if not _validateEmail(email):
            emailState = "Please provide a valid email address"
            return  redirect('/index/', emailState=emailState, email=email, username=username)
            
        password = _generatePassword()
        _sendEmail(username, email, password)
        PongUser.objects.create(username=username, email=email, password=password)
        
        authenticate(username, password)
        login(username, password)

        return redirect('/profile/edit', username=username)

    return  redirect('/index/', emailState=emailState, email=email, username=username)

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
    if not email.count('.') >= 1:
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
    
    Output:
        
    """
    taken = False
    try:
        user = User.objects.get(username=username)
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
    
    Output:
        
    """
    suggestions = []
    number = 0      
    while len(suggestions) < 5:
        suggestion = username + str(number)
        if not _usernameTaken(suggestion):
            suggestions += [suggestion]
        number += 1
            
    return suggestions


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


