from Game.models import Game
from Game.forms.confirmGameForm import ConfirmGameForm
from Utilities.game_utilities import obtainGamesToBeConfirmed
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
    #redirect to login if they haven't logged in
    if not request.user.is_authenticated():
        messages.add_message(request,messages.INFO,'Please Login')
        return redirect('/login/')
    
    #redirect to edit profile if they haven't filled in their profile details 
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    
    username = request.session['username']
    
    #obtain the Games and write them to the forms
    gamesToConfirm, gamesOthersConfirm = obtainGamesToBeConfirmed(username)
    confirmGameForms = []
    otherGameForms = []
    
    #store the Game data for Games the PongUser can verify (in forms)
    for game in gamesToConfirm:
        confirmForm = ConfirmGameForm()
        confirmForm.setGameData(game)
        confirmGameForms.append(confirmForm)
    
    #store the Game data for Games the PongUser's opponents can verify (in forms)
    for game in gamesOthersConfirm:
        otherForm = ConfirmGameForm()
        otherForm.setGameData(game)
        otherGameForms.append(otherForm)
    
    return render(request, 'game/confirm.html', { 'confirm_games': confirmGameForms, 'opponent_confirm_games': otherGameForms})