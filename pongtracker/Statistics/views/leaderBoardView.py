from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from User.models import Institution
from Statistics.models import LifeStats, Ranking


def leaderboardPage(request):
    if not request.user.is_authenticated():
         return redirect('/login/')
    
    
    return render(request,'statistics/leaderboard.html',{'username':request.session['username']})