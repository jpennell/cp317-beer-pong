from Game.models import Game
from django.shortcuts import redirect
from django.contrib import messages
from verifyGameView import isUserAllowedToVerifyGame

def confirmGame(request,game_id):
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
    
    username = request.session['username']
    game = _obtainGame(game_id)
    
    if game is None or not isUserAllowedToVerifyGame(game,username):
        message = "This is not a game that you are allowed to confirm"
    elif not _isGameEnded(game):
        message = "Game cannot be denied as it has not properly ended"
    elif game.getIsConfirmed():
        message = "Game already confirmed/denied"
    else:
        message = "Game " + game_id + " confirmed"
    
    messages.add_message(request,messages.INFO,message)
    return redirect('/game/verify')

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

def _isGameEnded(game):
    return True