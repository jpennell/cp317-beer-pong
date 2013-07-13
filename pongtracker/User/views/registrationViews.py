from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from User.models import Profile, Institution
from django.core.context_processors import csrf
from django.template import RequestContext



def registerNewUser(request):
    
    
    return



def _validateEmail(email):
    
    return True

def _validateUsername(username):
    
    return True

def suggestUsernames():


    return ['timmy5','timmy6']


def _sendEmail(username,email):
    password = _generatePasswor()
        
    return

def _generatePassword():
    password = "Bubbles"
    
    return password


