import trueskill
from Game.models import Game
from django.shortcuts import redirect
from django.contrib import messages
from utilities2 import obtainGame, isGameEnded, isUserAllowedToVerifyGame

def confirmGame(request,game_id):
    """
    Processes a Game's confirmation request

    Keyword arguments:
    request -- the HTTP request sent by the PongUser when they go to game/{game_id}/confirm
               on the PongTracker website.
    game_id -- the game_id of the Game the PongUser wants to confirm/deny 
    
    Contributors: Richard Douglas
    
    Output: redirects the PongUser to the verify game page with a message indicating the 
            state of the confirmation request.
            
            PongUsers are only allowed to confirm Games where they have played on the Team opposing
            the PongUser who created the Game. The Game must also exist, have ended, and not already
            have been confirmed/denied. 
        
    """
    if not request.user.is_authenticated():
        messages.add_message(request,messages.INFO,'Please Login')
        return redirect('/login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    
    username = request.session['username']
    game = obtainGame(game_id)
    
    if game is None or not isUserAllowedToVerifyGame(game,username):
        message = "That is not a game that you are allowed to confirm"
    elif not isGameEnded(game):
        message = "Game cannot be confirmed as it has not properly ended"
    elif game.getIsConfirmed():
        message = "Game already confirmed/denied"
    else:
        _confirmTheGame(game)
        message = "Game " + game_id + " confirmed"
    
    messages.add_message(request,messages.INFO,message)
    return redirect('/game/verify')

def _confirmTheGame(game):
    """
    Performs the overhead necessary to confirm a Game

    Keyword arguments:
    game -- the Game to be confirmed
    
    Contributors: Richard Douglas
    
    Output: LifeStats of the PongUsers who played the Game are updated
            to reflect the Events of the Game. 
            The Game is then marked as being confirmed/denied and kept in the database.
    """
    
    #get Teams and Users
    team1 = game.getTeam1()
    team2 = game.getTeam2()
    users = [team1.getUser1(),team1.getUser2(),team2.getUser1(),team2.getUser2()]
    
    #get Events
    events = game.getEvents()
    if not events: return
    cupEvents, endGameEvent = events[0:-1], events[-1]
    
    #process Events that involve cups being sunk
    for cupEvent in cupEvents:
        responsibleUser = cupEvent.getUser()
        stats = responsibleUser.getLifeStats()
        _updateCupShotStats(stats,event)
        _updateCupNumberStats(stats,event)
        #_updateStatsWithEvent(stats,cupEvent)
    return

def _updateCupShotStats(stats,event):
    """
    

    Keyword arguments:
    stats -- the LifeStats to update
    event -- the Event in which a cup was sunk
    
    Contributors: Richard Douglas
    
    Output: stats has its cup1sunk, cup2sunk... attributes
            updated if necessary
    """
    eventType = event.getEventType()
    whatHappened = eventType.getName()
    
    if (whatHappened == "bounce"):
        #stats.incBounceShots(1) etc...
        pass
    elif (whatHappened == "trick"):
        pass
    elif (whatHappened == "regular"):
        pass
    elif (whatHappened == "party_foul"):
        pass
    elif (whatHappened == "redemption"):
        pass
    elif (whatHappened == "death"):
        pass
    return

def _updateCupNumberStats(stats,event):
    """
    
    Keyword arguments:
    stats -- the LifeStats to update
    event -- the Event in which a cup was sunk
    
    Contributors: Richard Douglas
    
    Output: stats has its cup1sunk, cup2sunk... attributes
            updated if necessary
    """
    if (event.getCup1()):
        #stats.incCup1(1) etc...
        pass 
    if (event.getCup2()):
        pass
    if (event.getCup3()):
        pass
    if (event.getCup4()):
        pass
    if (event.getCup5()):
        pass
    if (event.getCup6()):
        pass
    return
    



