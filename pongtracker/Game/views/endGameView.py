from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from Game.models import Game, Team
from django.shortcuts import render, redirect
from Utilities.utilities import *
from django.template import Context

def viewGameSummaryRequest(request, game_id):
    
    username = request.session['username']
    
    game = Game.objects.get(pk=game_id)
    
    return render(request, 'game/summary.html')