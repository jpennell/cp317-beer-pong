import urllib
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
import string
import random
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError

    
"""----------------------------------------------
# Creates an HttpResponseRedirect based on url input 
# and keyword arg parameters
#
#    returns: HttpResponseRedirect
#----------------------------------------------"""

def redirect_with_params(url,**kwargs):
    params = urllib.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


def sendEmail(username, email, password,message):
    """
    sends a new user their temporary password

    Keyword arguments:
    username -- user's username (str)
    password -- user's temp password (str)
    email -- user's email (str)
    
    Contributors:
    Erin Cramer
    
    Output:
        
    """
    
    
    try:
        send_mail('Pong Tracker Account', message, 'thepongtracker@gmail.com', [email], fail_silently = False )
    except BadHeaderError:
        pass
    
    return


#----------------------------------------------
# Creates a random password of length len
# len: int length of password
#
# returns: string
#----------------------------------------------
def createRndPass(length):
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