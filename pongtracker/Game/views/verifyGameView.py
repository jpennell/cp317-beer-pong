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
    
    gamesToConfirm = _obtainGamesToConfirm(username)
    confirmGameForms = []
    for game in gamesToConfirm:
        form = ConfirmGameForm()
        _writeGameToForm(game,form)
        confirmGameForms.append(form)
    
    return render(request, 'game/confirm.html', { 'confirm_game_forms': confirmGameForms})

def _obtainGamesToConfirm(username):
    """
    Finds and returns the Games which the PongUser has played
    that need confirming/denying.

    Keyword arguments:
    username -- the username of the PongUser viewing the game/verify page  
    
    Contributors: Richard Douglas
    
    Output: a Python list of the Games that the PongUser is allowed to confirm/deny.
            This list is ordered by date with more recent Games going at the front.
        
    """
    allGames = Game.objects.all().order_by('-_datePlayed')
    
    gamesToConfirm = []
    for game in allGames:
        if _gameIsToBeConfirmedBy(game,username):
            gamesToConfirm.append(game)
    return gamesToConfirm

def _gameIsToBeConfirmedBy(game,username):
    """
    Determines whether the Game is meant to be confirmed/denied by the PongUser.

    Keyword arguments:
    game --  the Game we are checking
    username -- the username of the PongUser 
    
    Contributors: Richard Douglas
    
    Output: True if the PongUser is allowed to confirm/deny this Game, False otherwise.
            
            The PongUser is only allowed to confirm/deny Games that have ended, haven't already
            been confirmed/denied and in which they participated on the Team opposing the PongUser
            who created the Game.
        
    """
    if game.getIsConfirmed():
        needsConfirmation = False
    else:
        #only players on Team2 can confirm/deny the Game
        teamWhoConfirms = game.getTeam2()
        usersOnTeam = [teamWhoConfirms.getUser1(), teamWhoConfirms.getUser2()]
        usernamesOfUsers = [user.username for user in usersOnTeam]
        needsConfirmation = username in usernamesOfUsers
    return needsConfirmation


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
    usernames = [team1[0].username, team1[1].username,
                 team2[0].username, team2[1].username]
    
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