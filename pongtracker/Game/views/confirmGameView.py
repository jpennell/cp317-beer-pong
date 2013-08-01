#from trueskill import Rating, rate
from Game.models import Game
from django.shortcuts import redirect
from django.contrib import messages
from Utilities.game_utilities import obtainGame, isGameEnded, isUserAllowedToVerifyGame, obtainWinningTeam, obtainLosingTeam

TRUESKILL_IMPORTED = False #<----- change when you comment/uncomment the "from trueskill import ..." line

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
        message = "Game successfully confirmed"
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
    cupEvents = events[0:len(events) - 1]
    
    #process Events that involve cups being sunk
    for cupEvent in cupEvents:
        responsibleUser = cupEvent.getUser()
        stats = responsibleUser.getLifeStats()
        _updateCupShotStats(stats,cupEvent)
        _updateCupNumberStats(stats,cupEvent)
    
    winningTeam, losingTeam = obtainWinningTeam(game), obtainLosingTeam(game)
    _updateWinsAndLosses(winningTeam,losingTeam)
    if TRUESKILL_IMPORTED:
        _updateRankings(winningTeam,losingTeam)
    game.setIsConfirmed(True)
    game.save()
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
    stats.save()
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
    stats.save()
    return

def _updateWinsAndLosses(winningTeam,losingTeam):
    """
    Updates the win and loss statistics of the PongUsers who played the Game.
    
    PongUsers on winningTeam have their win statistics increased by 1.
    PongUsers on losingTeam have their loss statistics increased by 1. 
    
    Keyword arguments:
    winningTeam -- the Team who won the Game
    losingTeam -- the Team who lost the Game
    
    Contributors: Richard Douglas
    
    Output: None
    """
    winners = [winningTeam.getUser1(), winningTeam.getUser2()]
    losers = [losingTeam.getUser1(), losingTeam.getUser2()]
    
    for winner in winners:
        stats = winner.getLifeStats()
        stats.incWins(1)
        stats.save()
    
    for loser in losers:
        stats = loser.getLifeStats()
        stats.incLoses(1)
        stats.save()
    return

def _updateRankings(winningTeam,losingTeam):
    """
    Updates the Rankings of the PongUsers who played the Game.
    
    Keyword arguments:
    winningTeam -- the Team who won the Game
    losingTeam -- the Team who lost the Game
    
    Contributors: Richard Douglas
    
    Output: None
    """
    #obtain the Ranking objects
    winningRankings = _obtainRankings(winningTeam)
    losingRankings = _obtainRankings(losingTeam)
    
    #obtain the corresponding TrueSkill Rating objects
    oldWinningRatings = _obtainRatings(winningRankings)
    oldLosingRatings = _obtainRatings(losingRankings)
    
    #have TrueSkill rate the Game
    newWinningRatings, newLosingRatings = rate([oldWinningRatings,oldLosingRatings], ranks = [0,1])
    
     #update Ranking objects with their new Mu and Sigma values
    _writeRatingsToRankings(newWinningRatings,winningRankings)
    _writeRatingsToRankings(newLosingRatings,losingRankings)
    return

def _obtainRankings(team):
    """
    obtains the Ranking objects of the PongUsers on a Team.
    
    Keyword arguments:
    team -- the Team whose Ranking objects we want
    
    Contributors: Richard Douglas
    
    Output: rankings, a Python list of the Team's PongUser's Ranking objects
    """
    users = [team.getUser1(), team.getUser2()]
    rankings = [users[0].getRanking(), users[1].getRanking()]
    return rankings

def _obtainRatings(rankings):
    """
    obtains the (TrueSkill) Rating objects that correspond to Ranking objects.
    
    Keyword arguments:
    rankings -- a Python list of Ranking objects
    
    Contributors: Richard Douglas
    
    Output: ratings, a Python list of (TrueSkill) Rating objects 
                     that have the Mu and Sigma values of their corresponding Ranking objects
    """
    ratings = []
    for ranking in rankings:
        mu = ranking.getMu()
        sigma = ranking.getSigma()
        rating = Rating(mu,sigma)
        ratings.append(rating)
    return ratings

def _writeRatingsToRankings(ratings,rankings):
    """
    Updates the Ranking objects with the new Mu and Sigma values
    held by the (TrueSkill) Rating objects.
    
    Keyword arguments:
    ratings -- the (TrueSkill) Rating objects
    rankings -- the PongUsers' Ranking objects
    
    Contributors: Richard Douglas
    
    Output: None
    """
    for i in range(len(ratings)):
        mu = ratings[i].mu
        sigma = ratings[i].sigma
        rankings[i].setMu(mu)
        rankings[i].setSigma(sigma)
        rankings[i].save()
    return