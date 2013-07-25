from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from Game.models import Game, Team
from django.shortcuts import render, redirect
from Utilities.utilities import *
from django.template import Context

def scoreGame(request, game_id):
    if not request.user.is_authenticated():
        messages.add_message(request,message.INFO,'Please Login')
        return redirect('/login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    username = request.session['username']
    
    game = Game.objects.get(pk=game_id)
    
    return render(request, 'game/play.html')