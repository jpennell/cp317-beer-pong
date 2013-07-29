from Game.models import Game
from Game.forms.confirmGameForm import ConfirmGameForm
from django.shortcuts import render, redirect
from Utilities.utilities import *
from django.contrib import messages

def confirmOrDenyGame(request,game_id):
    """
    Processes a Game's confirmation/denial request

    Keyword arguments:
    request -- the HTTP request sent by the PongUser when they go to game/{game_id}/confirm
               on the PongTracker website.
    game_id -- the game_id of the Game the PongUser wants to confirm/deny 
    
    Contributors: Richard Douglas
    
    Output: for now, redirects the PongUser to the index page with a string indicating the 
            state of the confirmation/denial request.
        
    """
    if not request.user.is_authenticated():
        messages.add_message(request,messages.INFO,'Please Login')
        return redirect('/login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    
    game = _obtainGame(game_id)
    
    location = '/index/'
    if game is None:
        message = "Game " + game_id + " does not exist"
    elif request.method != "POST":
        message = "Access denied"
    else:
        form = ConfirmGameForm(data=request.POST)
        location = 'game/verify/'
        if not form.is_valid():
            message = "No choice selected"
        else:
            choice = form.cleaned_data['confirm']
            print choice
            if choice == 'confirm':
                message = "Confirming game " + game_id
            else:
                message = "Denying game " + game_id
    
    messages.add_message(request,messages.INFO,message)
    return redirect(location)

def _obtainGame(game_id):
    """
    Takes a game_id and find its corresponding Game.

    Keyword arguments:
    game_id -- a Game's id
    
    Contributors: Richard Douglas
    
    Output: the Game corresponding to the id or None if no such Game exists.
        
    """
    game = None
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        game = None
    return game