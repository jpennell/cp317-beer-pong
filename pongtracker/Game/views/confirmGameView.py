#import trueskill
from Game.models import Game
from django.shortcuts import redirect
from django.contrib import messages
from utilities2 import obtainGame, isGameEnded, isUserAllowedToVerifyGame, obtainWinningTeamLosingTeam

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
    
    #get Events
    events = game.getEvents()
    if not events: return """<----REMOVE THIS LINE WHEN Score Game IS READY"""
    cupEvents = events[:-1]
    
    #process Events that involve cups being sunk
    for cupEvent in cupEvents:
        responsibleUser = cupEvent.getUser()
        stats = responsibleUser.getLifeStats()
        _updateCupShotStats(stats,event)
        _updateCupNumberStats(stats,event)
    
    winningTeam, losingTeam = obtainWinningTeamLosingTeam(game)
    _updateWinsAndLosses(winningTeam,losingTeam)
    #_updateRankings(winningTeam,losingTeam)
    game.setConfirmed(True)
    return

def _updateCupShotStats(stats,event):
    """
    updates the statistics entries corresponding to
    eventtypes with the Event that occurred.

    Keyword arguments:
    stats -- the LifeStats to update
    event -- the Event in which a cup was sunk
    
    Contributors: Richard Douglas
    
    Output: None
    """
    eventType = event.getEventType()
    whatHappened = eventType.getName()
    
    if (whatHappened == "regular"):
        pass
    elif (whatHappened == "bounce"):
        stats.incBounceShots(1)
    elif (whatHappened == "trick"):
        stats.incTrickShots(1)
    elif (whatHappened == "party_foul"):
        stats.incPartyFouls(1)
    elif (whatHappened == "redemption"):
        stats.incRedemptions(1)
    elif (whatHappened == "death"):
        stats.incDeathCups(1)
    return

def _updateCupNumberStats(stats,event):
    """
    updates the cup1sunk, cup2sunk, etc...
    of LifeStats with the Event that occurred.
    
    Keyword arguments:
    stats -- the LifeStats to update
    event -- the Event in which a cup was sunk
    
    Contributors: Richard Douglas
    
    Output: None
    """
    if (event.getCup1()):
        stats.incCup1Sunk(1)
    if (event.getCup2()):
        stats.incCup2Sunk(1)
    if (event.getCup3()):
        stats.incCup3Sunk(1)
    if (event.getCup4()):
        stats.incCup4Sunk(1)
    if (event.getCup5()):
        stats.incCup5Sunk(1)
    if (event.getCup6()):
        stats.incCup6Sunk(1)
    return

def _updateWinsAndLosses(winningTeam,losingTeam):
    winners = [winningTeam.getUser1(), winningTeam.getUser2()]
    losers = [losingTeam.getUser1(), losingTeam.getUser2()]
    
    for winner in winners:
        stats = winner.getLifeStats()
        stats.incWins(1)
    
    for loser in losers:
        stats = loser.getLifeStats()
        stats.incLoses(1)
    return

#def _updateRankings(winningTeam,losingTeam):
#    #obtain the Ranking objects
#    winningRankings = _obtainRankings(winningTeam)
#    losingRankings = _obtainRankings(losingTeam)
#    
#    #obtain the corresponding TrueSkill Rating objects
#    oldWinningRatings = _obtainRatings(winningRankings)
#    oldLosingRatings = _obtainRatings(losingRankings)
#    
#    #have TrueSkill rate the Game
#    newWinningRatings, newLosingRatings = trueskill.rate([oldWinningRatings,oldLosingRatings], ranks = [0,1])
#    
#     #update Ranking objects with their new Mu and Sigma values
#    _writeRatingsToRankings(newWinningRatings,winningRankings)
#    _writeRatingsToRankings(newLosingRatings,losingRankings)
#    return
#
#def _obtainRankings(team):
#    users = [team.getUser1(), team.getUser2()]
#    rankings = [users[0].getRanking(), users[1].getRanking()]
#    return rankings
#
#def _obtainRatings(rankings):
#    ratings = []
#    for ranking in rankings:
#        mu = ranking.getMu()
#        sigma = ranking.getSigma()
#        rating = trueskill.Rating(mu,sigma)
#        ratings.append(rating)
#    return ratings
#
#def _writeRatingsToRankings(ratings,rankings):
#    for i in range(len(ratings)):
#        mu = ratings[i].getMu()
#        sigma = ratings[i].getSigma()
#        rankings[i].setMu(mu)
#        rankings[i].setSigma(sigma)
#    return