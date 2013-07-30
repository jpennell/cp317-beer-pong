from Game.models import Game
from Game.forms.confirmGameForm import ConfirmGameForm
from django.shortcuts import render, redirect
from django.contrib import messages

def verifyGameRequest(request):
    """
    Displays the verify game page where PongUsers can choose Games to confirm/deny.
    
    Keyword arguments:
    request -- the HTTP request sent by the PongUser when they go to game/verify
               on the PongTracker website
    
    Contributors: Richard Douglas
    
    Output: renders the webpage based on what Games the PongUser has to confirm.
        
    """
    if not request.user.is_authenticated():
        messages.add_message(request,messages.INFO,'Please Login')
        return redirect('/login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    
    username = request.session['username']

    gamesToConfirm, gamesOthersConfirm = _obtainGamesToBeConfirmed(username)
    confirmGameForms = []
    otherGameForms = []
    
    for game in gamesToConfirm:
        newData = ConfirmGameForm(game)
        confirmGameForms.append(newData)
    
    for game in gamesOthersConfirm:
        newData = ConfirmGameForm(game)
        otherGameForms.append(newData)
    
    return render(request, 'game/confirm.html', { 'confirm_games': confirmGameForms, 'opponent_confirm_games': otherGameForms})

def _obtainGamesToBeConfirmed(username):
    """
    Finds and returns the Games which the PongUser has played
    that need confirming/denying.

    Keyword arguments:
    username -- the username of the PongUser viewing the game/verify page  
    
    Contributors: Richard Douglas
    
    Output: gamesToConfirm -- a Python list of Games that the User is to confirm/deny
            gamesOthersConfirm -- a Python list of Games that the opposing Team is to confirm/deny
        
    """
    allGames = Game.objects.all().order_by('-_datePlayed')
    
    gamesToConfirm = []
    gamesOthersConfirm = []
    
    for game in allGames:
        if game.getIsConfirmed():
            continue
        elif _isUserOnTeam(game.getTeam2(), username):
            gamesToConfirm.append(game)
        elif _isUserOnTeam(game.getTeam1(), username):
            gamesOthersConfirm.append(game)
    return gamesToConfirm, gamesOthersConfirm

def _isUserOnTeam(team, username):
    """
    Determines whether the PongUser is on this particular Team.
    
    Keyword arguments:
    team -- the Team we are checking
    username -- the username of the PongUser
    
    Contributors: Richard Douglas
    
    Output: True if the PongUser is on the Team, False otherwise.
    """
    teamUsers = [team.getUser1(), team.getUser2()]
    teamUsernames = [teamUser.getUsername() for teamUser in teamUsers]
    return username in teamUsernames

def isUserAllowedToVerifyGame(game,username):
    return _isUserOnTeam(game.getTeam2(),username) 