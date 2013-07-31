from User.models import *
from Game.models import Game, Team, Event
from django.shortcuts import render, redirect, HttpResponse
from Utilities.utilities import *
from django.template import Context
import json



def infoGameRequest(request, game_id):

    

    game = Game.objects.get(id=game_id)
    
    jsonGame = _gameToJSON(game)
    return HttpResponse(jsonGame)

    


def _gameToJSON(game):

    events = Event.objects.filter(_game_id=game.getID())
    team1User1 = game.getTeam1().getUser1().getUsername()
    team1User2 = game.getTeam1().getUser2().getUsername()
    team2User1 = game.getTeam2().getUser1().getUsername()
    team1User2 = game.getTeam2().getUser2().getUsername()
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

    for event in events:
        print(event.getUser().getUsername)
        print(team1User1)
        print(team1User2)
        if event.getUser().getUsername()==team1User1 or event.getUser().getUsername()==team1User2:
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
        else:
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
    
    dictTeam1 = {'team1User1':team1User1,'team1User2':team1User2,
     'team1Cup1':team1Cup1,'team1Cup2':team1Cup2,'team1Cup3':team1Cup3,
     'team1Cup4':team1Cup4,'team1Cup5':team1Cup5,'team1Cup6':team1Cup6,}
    
    dictTeam2 = {'team2User1':team2User1,'team2User2':team2User2,
     'team2Cup1':team2Cup1,'team2Cup2':team2Cup2,'team2Cup3':team2Cup3,
     'team2Cup4':team2Cup4,'team2Cup5':team2Cup5,'team2Cup6':team2Cup6}
    
    dictGame = {'team1':dictTeam1,'team2':dictTeam2}
    return json.dumps(dictGame,indent=5,sort_keys=True)