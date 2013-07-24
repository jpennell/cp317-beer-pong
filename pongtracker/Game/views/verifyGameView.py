from Game.models import Game
from Game.forms.confirmGameForm import ConfirmGameForm
from django.shortcuts import render, redirect

def verifyGameRequest(request):
    username = request.session['username']
    
    if request.method == 'POST':
        form = ConfirmGameForm(data=request.POST)
        if form.is_valid():
            choice = form.cleaned_data['confirm']
    
    gamesToConfirm = obtainGamesToConfirm(username)
    confirmGameForms = []
    for game in gamesToConfirm:
        form = ConfirmGameForm()
        writeGameToForm(game,form)
        confirmGameForms.append(form)
    
    return render(request, 'game/confirm.html', { 'confirm_game_forms': confirmGameForms})

def obtainGamesToConfirm(username):
    allGames = Game.objects.all().order_by('-date_played')
    
    gamesToConfirm = []
    for game in allGames:
        if isToBeConfirmed(game,username):
            gamesToConfirm.append(game)
            print game.pk
    return gamesToConfirm

def isToBeConfirmed(game,username):
    teamWhoConfirms = game.team2
    usersOnTeam = [teamWhoConfirms.user1, teamWhoConfirms.user2]
    usernamesOfUsers = [user.username for user in usersOnTeam]
    return username in usernamesOfUsers

def writeGameToForm(game,form):
    #obtain the usernames
    teams = [game.team1,game.team2]
    team1 = [teams[0].user1,teams[0].user2]
    team2 = [teams[1].user1,teams[1].user2]
    usernames = [team1[0].username, team1[1].username,
                 team2[0].username, team2[1].username]
    
    #store the usernames in the form
    form.player1 = usernames[0]
    form.player2 = usernames[1]
    form.player3 = usernames[2]
    form.player4 = usernames[3]
    
    #also write the date to the form
    form.date_played = game.date_played
    #lastly write the game_id so that the form knows which page to go to
    form.game_id = game.pk
    return