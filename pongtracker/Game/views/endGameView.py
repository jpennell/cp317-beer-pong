from User.models import *
from Game.models import Game, Team, Event
from Statistics.models import RankView, Ranking
from django.shortcuts import render, redirect
from Utilities.utilities import *
from django.template import Context
from Game.forms.endGameForm import EndGameForm
from Statistics.views.leaderBoardView import *

def viewGameSummaryRequest(request, game_id):
    
    if not request.user.is_authenticated():
        messages.add_message(request,message.INFO,'Please Login')
        return redirect('/login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    
    form = EndGameForm()

    currUsername = request.session['username']
    currUser = PongUser.objects.get(username=currUsername)
    
    game = Game.objects.get(pk=game_id)
    
    users = [game.getTeam1().getUser1(), game.getTeam1().getUser2(), game.getTeam2().getUser1(), game.getTeam2().getUser2()]
    
    if currUser in users:
        
        form.authErr = False
        
        stats = []
        events = Event.objects.filter(_game=game_id, _eventTime__gte=game.getDatePlayed())
        
        for x in range(len(users)):
            form.usernames[x] = users[x].getUsername()
            form.ranks[x] = getUserRank(users[x])
            stats.append(_getStats(users[x], events, game_id))     
            
        form.stats = stats
        
    else:
        
        form.authErr = True
        
    return


def _getStats(user, events, game_id):
    
    sunk = 0
    tricks = 0
    bounces = 0
    fouls = 0
    redemptions = 0
    
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
    
    return [sunk,tricks,bounces,fouls,redemptions]
