from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from User.models import Institution
from django.core.context_processors import csrf
from django.template import RequestContext

def editProfile( request ):
    """{{Description}}

    Keyword arguments:
    variable -- description
    variable -- description

    Contributors:
    Quinton Black

    Output:

    """


    return render( request, 'user/editProfile.html', {'username': username} )

def _updatePassword( password ):

    return

def _updateUser( username, password, firstName, lastName, email, height, yearOfGradution, userProfilePhoto, isBanned ):



    return

