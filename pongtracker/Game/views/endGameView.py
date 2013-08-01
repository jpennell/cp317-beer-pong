from User.models import *
from Game.models import Game, Team, Event
from Statistics.models import RankView, Ranking
from django.shortcuts import render, redirect
from Utilities.utilities import *
from django.template import Context
from Game.forms.endGameForm import EndGameForm
from Statistics.views.leaderBoardView import *

def viewGameSummaryRequest(request, game_id):
    
    #check if user is logged in
    if not request.user.is_authenticated():
        messages.add_message(request,message.INFO,'Please Login')
        return redirect('/login/')
    
    #check if user has updated profile
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    
    #get form
    form = EndGameForm()
    
    #get current user
    currUsername = request.session['username']
    currUser = PongUser.objects.get(username=currUsername)
    
    #get game object
    game = Game.objects.get(pk=game_id)
    
    #get users
    users = [game.getTeam1().getUser1(), game.getTeam1().getUser2(), game.getTeam2().getUser1(), game.getTeam2().getUser2()]
    
    #if the current user is one of the users in the game, show results
    if currUser in users:
        #no authorization error
        form.authErr = False
        
        stats = []
        
        #get list of events from the game
        events = Event.objects.filter(_game=game_id, _eventTime__gte=game.getDatePlayed())
        
        #go through users
        for x in range(len(users)):
            #get username
            form.users[x] = users[x]
            #get the users rank
            form.ranks[x] = getUserRank(users[x])
            #tally statistics for each user
            stats.append(_getStats(users[x], events))     
            
        #get winner of game
        form.winner = _getWinner(game, events)
        
        form.stats = stats
        
    else:
        
        #if the logged in user is not one of the players in the game, do not let them see the summary
        form.authErr = True
        
    return render(request, 'game/summary.html', {'form': form})


def _getWinner(game, events):
    """ gets winner of a game based on win event

    Keyword arguments:
    game -- game object
    events -- list of events from the game
    
    Contributors: 
    Matt Hengeveld
    
    Output:
    winner -- number of team of winner; if the winner is not able to be
              determined, 0 is returned
        
    """
    team1 = game.getTeam1()
    team2 = game.getTeam2()
    
    user = None
    
    for x in range(len(events)):
        event = events[x].getEventType().getName()
        if event == 'win':
            user = events[x].getUser()
            
    if (user == team1.getUser1()) or (user == team1.getUser2()):
        winner = 1
    elif (user == team2.getUser1()) or (user == team2.getUser2()):
        winner = 2
    else:
        winner = 0
    
    return winner


def _getStats(user, events):
    """ tallies stats for given user, from given game

    Keyword arguments:
    user -- PongUser object
    events -- list of events from the game
    
    Contributors: 
    Matt Hengeveld
    
    Output:
    list -- [sunk,tricks,bounces,fouls,death,redemptions]
        
    """
    sunk = 0
    tricks = 0
    bounces = 0
    fouls = 0
    redemptions = 0
    death = 0
    
    for x in range(len(events)):
        if (events[x].getUser() == user):
            event = events[x].getEventType().getName()
            if event == 'regular':
                sunk += 1
            elif event == 'trick':
                tricks += 1
            elif event == 'bounce':
                bounces += 1
            elif event == 'party_foul':
                fouls += 1
            elif event == 'redemption':
                redemptions += 1
            elif event == 'death':
                death+=1
    return [sunk,tricks,bounces,fouls,death,redemptions]
