import urllib
from django.http import HttpResponseRedirect
import string
import random
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from types import *

    

def redirect_with_params(url,**kwargs):
    """   Creates an HttpResponseRedirect based on url input 

    Keyword arguments:
    url -- url to post to (String)
    **kwarfs -- any additional parameters
    
    Contributors:
    Erin Cramer
    
    Output:
        HttpResponseRedirect
    """
    params = urllib.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


def sendEmail(username, email, password,message):
    """Sends a new user their temporary password

    Keyword arguments:
    username -- user's username (String)
    password -- user's temp password (String)
    email -- user's email (String)
    message -- the message to send (String)
    
    Contributors:
    Erin Cramer
    Quinton Black
    
    Output:
        
    """
    try:
        send_mail('Pong Tracker Account', message, 'thepongtracker@gmail.com', [email], fail_silently = False )
    except BadHeaderError:
        pass
    
    return


def createRndPass(length):
    """   Creates a random password of a given length

    Keyword arguments:
    length -- length of password to provide
    
    Contributors:
    Erin Cramer
    
    Output:
        rndPass - a random password
    """
    assert type(length) is IntType, "length must be an integer" 
    
    passChars = list(string.ascii_letters + string.digits) #list of lowercase, uppercase and digits
    passChars.remove('l') #remove characters that look similar to others
    passChars.remove('O')
    
    random.seed() #generate random seed based on time
    
    rndPass = ''
    for x in range(length): #create password
        rndPass += random.choice(passChars)
    
    return rndPass

def generatePassword():
    """
    generates a temp password for a user
    
    Contributors:
    Quinton Black
    
    Output:
    password - user's new password (str)   
    """
    password = createRndPass(8)

    return password