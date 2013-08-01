from Game.models import Game
from django.shortcuts import redirect
from django.contrib import messages
from Utilities.game_utilities import obtainGame, isGameEnded, isUserAllowedToVerifyGame 

def denyGame(request,game_id):
    """
    Processes a Game's denial request

    Keyword arguments:
    request -- the HTTP request sent by the PongUser when they go to game/{game_id}/deny
               on the PongTracker website.
    game_id -- the game_id of the Game the PongUser wants to deny 
    
    Contributors: Richard Douglas
    
    Output: redirects the PongUser to the verify game page with a message indicating the 
            state of the denial request.
            
            PongUsers are only allowed to deny Games where they have played on the Team opposing
            the PongUser who created the Game. The Game must also exist, have ended, and not already
            have been confirmed/denied. 
    """
    #redirect to login page if the PongUser is not logged in
    if not request.user.is_authenticated():
        messages.add_message(request,messages.INFO,'Please Login')
        return redirect('/login/')
     
    #redirect to edit profile page if the PongUser hasn't edited their profile 
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    
    username = request.session['username']
    game = obtainGame(game_id)
    
    if game is None or not isUserAllowedToVerifyGame(game,username):
        message = "That is not a game that you are allowed to deny"
    elif not isGameEnded(game):
        message = "Game cannot be confirmed as it has not properly ended"
    elif game.getIsConfirmed():
        message = "Game already confirmed/denied"
    else:
        _denyTheGame(game)
        message = "Game successfully denied"
        
    messages.add_message(request,messages.INFO,message)
    return redirect('/game/verify')

def _denyTheGame(game):
    """
    Performs the overhead necessary to deny a Game

    Keyword arguments:
    game -- the Game to be denied
    
    Contributors: Richard Douglas
    
    Output: game is marked as being confirmed/denied without anyone's LifeStats 
            being updated and is still kept in the database.
    """
    game.setIsConfirmed(True)
    game.save()
    return