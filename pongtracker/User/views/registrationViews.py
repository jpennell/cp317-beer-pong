from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from User.models import Profile
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.mail import send_mail


def registerNewUser( request ):
    username = email = ""
    emailState = ""
    usernameState = ""

    if request.POST:
        username = request.POST.get( 'username' )
        email = request.POST.get( 'email' )


        if not _validateUsername( username ):
            usernameState = "That is not a valid username"
            return  render_to_response( 'user/index.html', {'usernameState':usernameState, 'email':email, 'username':username},
                                       context_instance = RequestContext( request ) )

        user = User.objects.get( username = username )
        if user is None:
            usernameSuggestions = _suggestUsernames( username )


        #handle username schenaganaes

        if not _validateEmail( email ):
            emailState = "Please provide a valid email address"
            return  render_to_response( 'user/index.html', {'emailState':emailState, 'email':email, 'username':username},
                                       context_instance = RequestContext( request ) )

        _sendEmail( username, email )

        return render_to_response( 'user/editProfile.html', {'username':username, 'email':email}, context_instance = RequestContext( request ) )

    return  render_to_response( 'user/index.html', context_instance = RequestContext( request ) )



def _validateEmail( email ):

    return True

def _validateUsername( username ):

    return True

def _suggestUsernames( username ):


    return ['timmy5', 'timmy6']


def _sendEmail( username, email ):
    password = _generatePassword()

#    send_mail( 'Pong Tracker Account', "Here is your temporary password:{0}".format( password ),
#               email, ['from@hotmail.com'], fail_silently = False )

    return

def _generatePassword():
    password = "Bubbles"

    return password


