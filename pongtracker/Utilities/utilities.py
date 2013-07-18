import urllib
from django.http import HttpResponseRedirect
import string
import random
from django.contrib.auth import authenticate, login

SUCCESS = 'success'
INCORRECT = 'incorrect'
BANNED = 'banned'
    
"""----------------------------------------------
# Creates an HttpResponseRedirect based on url input 
# and keyword arg parameters
#
#    returns: HttpResponseRedirect
#----------------------------------------------"""



def redirect_with_params(url,**kwargs):
    params = urllib.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


#----------------------------------------------
# Creates a random password of length len
#    len:    int    length of password
#
#    returns: string
#----------------------------------------------
def createRndPass(length):
    passChars = list(string.ascii_letters + string.digits)    #list of lowercase, uppercase and digits
    passChars.remove('l')   #remove characters that look similar to others
    passChars.remove('O')
    
    random.seed()   #generate random seed based on time
    
    rndPass = ''
    for x in range(length):     #create password
        rndPass += random.choice(passChars)
    
    return rndPass


def loginUser(username, password, request):
    
    """{{Description}}

    Keyword arguments:
    variable -- description
    variable -- description

    Contributors:
    Quinton Black
    Erin Cramer

    Output:

    """
    
    user = authenticate( username = username, password = password )
    if user is not None:
        if user.getIsActive() and not user.getIsBanned():
            login( request, user )
            request.session['username'] = username
            return SUCCESS
        return BANNED
    else:
        return INCORRECT 