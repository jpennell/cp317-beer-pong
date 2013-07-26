from Game.models import Game
from Game.forms.confirmGameForm import ConfirmGameForm
from django.shortcuts import render, redirect
from Utilities.utilities import *

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
        messages.add_message(request,message.INFO,'Please Login')
        return redirect('/login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    
    game = _obtainGame(game_id)
    
    
    state = ""
    if game is None:
        state = "game " + game_id + " does not exist"
    elif request.method != "POST":
        state = "how did you get here?"
    else:
        form = ConfirmGameForm(data=request.POST)
        if not form.is_valid():
            state = "no choice selected"
        else:
            choice = form.cleaned_data['confirm']
            print choice
            if choice == 'confirm':
                state = "confirming game " + game_id
            else:
                state = "denying game " + game_id
    
    return redirect_with_params('/index/',state = state)

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