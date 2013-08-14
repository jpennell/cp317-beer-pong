from User.models import *
from Game.models import Game, Team, Event
from django.shortcuts import render, redirect, HttpResponse, Http404
from Utilities.utilities import *
from django.template import Context
import json
from django.conf import settings

def infoGameRequest( request, game_id ):

    try:
        game = Game.objects.get( id = game_id )
        jsonGame = _gameToJSON( game )
        return HttpResponse( jsonGame )
    except:
        raise Http404



def _gameToJSON( game ):
    events = Event.objects.filter( _game_id = game.getID() )
    team1User1 = game.getTeam1().getUser1().getUsername()
    team1User2 = game.getTeam1().getUser2().getUsername()
    team2User1 = game.getTeam2().getUser1().getUsername()
    team2User2 = game.getTeam2().getUser2().getUsername()
    team1Cup1 = False
    team1Cup2 = False
    team1Cup3 = False
    team1Cup4 = False
    team1Cup5 = False
    team1Cup6 = False
    team2Cup1 = False
    team2Cup2 = False
    team2Cup3 = False
    team2Cup4 = False
    team2Cup5 = False
    team2Cup6 = False

    try:
        lastEvent = Event.objects.filter( _game_id = game.getID ).order_by( '-id' )[0]
        is_over = str( lastEvent.getEventType() ) == 'win'
    except IndexError:  # this occurs when there are no events for the game yet
        is_over = False

    for event in events:
        ''' event types
        1    regular
        2    trick
        3    bounce
        4    party_foul
        5    redemption
        6    death
        7    win
        '''
        event_type = event.getEventType()

        user_on_team1 = event.getUser().getUsername() in [team1User1, team1User2]
        # if party foul, flip the team attribution
        if str( event_type ) == 'party_foul':
            user_on_team1 = not user_on_team1

        # have to switch the teams in order to get the cup attribution switched properly
        if user_on_team1:
            if event.getCup1():
                team2Cup1 = True
            if event.getCup2():
                team2Cup2 = True
            if event.getCup3():
                team2Cup3 = True
            if event.getCup4():
                team2Cup4 = True
            if event.getCup5():
                team2Cup5 = True
            if event.getCup6():
                team2Cup6 = True
        else:
            if event.getCup1():
                team1Cup1 = True
            if event.getCup2():
                team1Cup2 = True
            if event.getCup3():
                team1Cup3 = True
            if event.getCup4():
                team1Cup4 = True
            if event.getCup5():
                team1Cup5 = True
            if event.getCup6():
                team1Cup6 = True

    dictTeam1 = {'user1':team1User1, 'user2':team1User2,
     'cup1':team1Cup1, 'cup2':team1Cup2, 'cup3':team1Cup3,
     'cup4':team1Cup4, 'cup5':team1Cup5, 'cup6':team1Cup6, }

    dictTeam2 = {'user1':team2User1, 'user2':team2User2,
     'cup1':team2Cup1, 'cup2':team2Cup2, 'cup3':team2Cup3,
     'cup4':team2Cup4, 'cup5':team2Cup5, 'cup6':team2Cup6}

    dictGame = {'is_over': is_over, 'team1':dictTeam1, 'team2':dictTeam2}
    return json.dumps( dictGame, indent = 5, sort_keys = True )
