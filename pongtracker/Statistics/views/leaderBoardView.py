from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from User.models import Profile, Institution
from Statistics.models import LifeStats, Ranking


def leaderboardPage(request):
    
    
    return render_to_response('statistics/leaderboard.html',{username:request.session['username']})