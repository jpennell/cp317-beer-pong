from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from User.models import *
from Statistics.forms.leaderboardForm import LeaderboardForm
from Statistics.models import LifeStats, Ranking, RankView
from django.contrib import messages
from Utilities.utilities import *
from django.conf import settings

def leaderboardPage(request):
    """ handles the leaderboard

    Keyword arguments:
    request - the request for the leaderboard
    
    Contributors:
    Matthew Hengeveld

    """
    form = LeaderboardForm()
    
    if not request.user.is_authenticated():
        messages.add_message(request,messages.INFO,'Please Login')
        return redirect(settings.SITE_URL+'login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect(settings.SITE_URL+'profile/edit')
    
    username = request.session['username']
    
    #get the top ranked overall and display it by default
    topRanked = getTopRanked(10)
    
    #push list to the form
    displayBoard(topRanked,form)
    
    if request.method == 'POST':
        
        #get form information
        form = LeaderboardForm(request.POST)
        
        #get filter choice
        filterChoice = request.POST['filterSelect']
        
        #push a blank list to the form
        _blankBoard(form)

        
        #if the user chooses 'Overall', display the top ranked users
        if filterChoice == form.choices[0]:
            displayBoard(topRanked,form)
        else:   #display the top ranked from selected institution
      
            instLeaders = getInstitutionLeaders(10, filterChoice)
            displayBoard(instLeaders, form)
                       
        return render(request, 'statistics/leaderboard.html', {'form':form})
        
    else:

        return render(request, 'statistics/leaderboard.html', {'form':form})
    
def _blankBoard(form):
    """ clears the leaderboard form

    Keyword arguments:
    form -- leaderboard form
    
    Contributors:
    Matthew Hengeveld

    """
    for x in range(len(form.leaders)):
        form.leaders[x] = ''
        
    return

def displayBoard(topRanked, form):
    """ puts the top ten leaders into the leaderboard form

    Keyword arguments:
    topRanked -- list of the top ranked players, in order of rank
    form -- leaderboard form
    
    Contributors:
    Matthew Hengeveld

    """
    for x in range(len(topRanked)):
        user = topRanked[x]
        rank = getUserRank(user)
        name = user.username
        inst = user.getInstitution()
        
        userStats = user.getLifeStats()
        won = userStats.getWins()
        lost = userStats.getLoses()
        sunk = getTotalSunk(userStats)
        
        form.leaders[x] = [rank,name,inst,won,lost,sunk]
    
    return

def getTotalSunk(s):
    """
    This method calculates the total number of cups sunk by a player

    Keyword arguments:
    s -- lifeStats object of a user
    
    Contributors:
    Matthew Hengeveld
    
    Output:
    total -- total number of cups sunk
    """
    total = 0
    
    cupsTally = [s.getCup1Sunk(),s.getCup2Sunk(),s.getCup3Sunk(),s.getCup4Sunk(),s.getCup5Sunk(),s.getCup6Sunk()]
    
    for x in cupsTally:
        total += x
    
    return total

def getTopRanked(limit):
    """
    This method finds and retrieve's the top ranked users

    Keyword arguments:
    limit -- limit of how many top ranked users to get
    
    Contributors:
    Matthew Hengeveld
    
    Output:
    topRanked -- list of top ranked (in order)
    """
    topUsers = RankView.objects.order_by('-_skillNumber','-id')[:10]
    topRanked = []
    
    x=0
    while x <limit and x<len(topUsers):
        user_id = topUsers[x].user_id
        user = PongUser.objects.get(id=user_id)
        topRanked.append(user)
        x+=1

    return topRanked

def getInstitutionRank(user):
    """
    This method finds and retrieve's a User's ranking within their own institution

    Keyword arguments:
    user -- PongUser object
    
    Contributors:
    Matt Hengeveld
    
    Output:
    rank -- the rank of the user at his or her institution (int)
    """
    rank = 1
    found = False
    count = 1
    querySize = 1000
    user_id = user.id
    institution = user.getInstitution()
    
    while not found or (size < 1):
        min = (count-1)*querySize
        max = (count*querySize)-1
        institutionUserRankViews = RankView.objects.order_by('-_skillNumber','-id').filter(user___institution___name=institution)[min:max]
        if (len(institutionUserRankViews) < max):
            size = len(institutionUserRankViews)
        else:
            size = querySize
        for x in range(size):
            queryUser = PongUser.objects.get(id=institutionUserRankViews[x].id)
            if (queryUser == user):
                found = True
                break
            else:
                rank += 1
        count += 1
    
    return rank

    
def getInstitutionLeaders(numberOfLeaders, institutionName):
    """
    This method retrieves a list of length numberOfUsers of the top ranking users at institution specified
    Keyword arguments:
    numberOfUsers -- The number of users to return (int)
    intitutionName -- the name of the institution (String)
     
    Contributors:
    Matthew Hengeveld
    
    Output:
    list of leaders -- [leader1(PongUser),leader2...]
    """

    userRanks = RankView.objects.order_by('-_skillNumber','-id').filter(user___institution___name=institutionName)[:numberOfLeaders]

    leaders=[]
    x=0
    while x <numberOfLeaders and x<len(userRanks):
        user_id = userRanks[x].user_id
        user = PongUser.objects.get(id=user_id)
        leaders.append(user)
        x+=1

    return leaders
    
def getUserRank(user):
    """
    This method retrieves the overall rank of a user
    Keyword arguments:
    user -- user to get rank of
     
    Contributors:
    Matthew Hengeveld
    
    Output:
    rank -- rank of user (int)
    """
    rank = None
    page = 1
    querySize = 1000
    user_id = user.id
    
    
    while rank == None:
        min = (page-1)*querySize
        max = (page*querySize)-1
        userRanks = RankView.objects.order_by('-_skillNumber','-id')[min:max]
        if (len(userRanks) < max):
            size = len(userRanks)
        else:
            size = querySize
        for x in range(size):
            if (userRanks[x].user_id == user_id):
                rank = x+((page-1)*querySize)
        page += 1
    
    return rank + 1
