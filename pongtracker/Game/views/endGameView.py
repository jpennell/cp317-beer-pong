from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from Game.models import Game, Team, Event
from Statistics.models import RankView, Ranking
from django.shortcuts import render, redirect
from Utilities.utilities import *
from django.template import Context
from Game.forms.endGameForm import EndGameForm
from Statistics.views.leaderBoardView import *

def viewGameSummaryRequest(request, game_id):
    
    form = EndGameForm
    currUsername = ''
    currUser = None
    
    try:
        currUsername = request.session['username']
        currUser = get_user_model().objects.get(username=currUsername)
    except:
        pass

    game = Game.objects.get(pk=game_id)
    
    users = [game.team1.user1, game.team1.user2, game.team2.user1, game.team2.user2]
        
    if currUser in users:
        
        form.authErr = False
        
        stats = []
        events = Event.objects.filter(game_id=game_id, event_time__lte=game.date_played)
        
        for x in range(len(users)):
            form.usernames[x] = users[x].username
            form.ranks[x] = getUserRank(users[x])
            stats.append(_getStats(users[x], events, game_id))     
            
        form.stats = stats
        
    else:
        
        form.authErr = True
        
    return render(request, 'game/summary.html', {'form':form})


def _getStats(user, events, game_id):
    
    sunk = 0
    tricks = 0
    bounces = 0
    fouls = 0
    redemptions = 0
    
    for x in range(len(events)):
        if (events[x].user == user):
            if events[x].event_type.typeName == 'sunk':
                sunk += 1
            elif events[x].event_type.typeName == 'trick':
                tricks += 1
            elif events[x].event_type.typeName == 'bounce':
                bounces += 1
            elif events[x].event_type.typeName == 'foul':
                fouls += 1
            elif events[x].event_type.typeName == 'redemption':
                redemptions += 1
    
    return [sunk,tricks,bounces,fouls,redemptions]

def _getRank(user):
    userRank = Ranking.objects.get(user=user)
    
    return userRank.rank