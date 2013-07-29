from Game.models import Game
from Game.forms.confirmGameForm import ConfirmGameForm
from django.shortcuts import render, redirect

def verifyGameRequest(request):
    """
    Displays the verify game page where PongUsers can choose Games to confirm/deny.
    
    Keyword arguments:
    request -- the HTTP request sent by the PongUser when they go to game/verify
               on the PongTracker website
    
    Contributors: Richard Douglas
    
    Output: renders the webpage based on what Games the PongUser has to confirm.
        
    """
    username = request.session['username']

    gamesToConfirm, gamesOthersConfirm = _obtainGamesToBeConfirmed(username)
    confirmGameForms = []
    otherGameForms = []

    for game in gamesToConfirm:
        form = ConfirmGameForm()
        _writeGameToForm(game, form)
        confirmGameForms.append(form)

    for game in gamesOthersConfirm:
        form = ConfirmGameForm()
        _writeGameToForm(game, form)
        otherGameForms.append(form)
    
    return render(request, 'game/confirm.html', { 'confirm_game_forms': confirmGameForms, 'other_games': otherGameForms})

def _obtainGamesToBeConfirmed(username):
    """
    Finds and returns the Games which the PongUser has played
    that need confirming/denying.

    Keyword arguments:
    username -- the username of the PongUser viewing the game/verify page  
    
    Contributors: Richard Douglas
    
    Output: gamesToConfirm -- a Python list of Games that the User can confirm/deny
            gamesOthersConfirm -- a Python list of Games that the opposing Team can confirm/deny
        
    """
    allGames = Game.objects.all().order_by('-_datePlayed')
    
    gamesToConfirm = []
    gamesOthersConfirm = []
    
    for game in allGames:
        if _userOnTeam(game.getTeam2(), username):
            gamesToConfirm.append(game)
        elif _userOnTeam(game.getTeam1(), username):
            gamesOthersConfirm.append(game)
    return gamesToConfirm, gamesOthersConfirm

def _userOnTeam(team, username):
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

def _writeGameToForm(game,form):
    """
    Passes Game data to the ConfirmGameForm so that it can display it
    in the HTML page.

    Keyword arguments:
    game -- the Game to get data from
    form -- the ConfirmGameForm to write the data to
    
    Contributors: Richard Douglas
    
    Output: None
    """
    #obtain the usernames
    teams = [game.getTeam1(),game.getTeam2()]
    team1 = [teams[0].getUser1(),teams[0].getUser2()]
    team2 = [teams[1].getUser1(),teams[1].getUser2()]
    usernames = [team1[0].getUsername(), team1[1].getUsername(),
                 team2[0].getUsername(), team2[1].getUsername()]
    
    #store the usernames in the form
    form.player1 = usernames[0]
    form.player2 = usernames[1]
    form.player3 = usernames[2]
    form.player4 = usernames[3]
    
    #also write the date to the form
    form.date_played = game.getDatePlayed()
    #lastly write the game_id so that the form knows which page to go to
    form.game_id = game.pk
    return