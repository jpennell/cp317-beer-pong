from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from User.models import *
from Statistics.forms.leaderboardForm import LeaderboardForm
from Statistics.models import LifeStats, Ranking, RankView
from django.contrib import messages
from Utilities.utilities import *


def leaderboardPage(request):
    form = LeaderboardForm()
    
    if not request.user.is_authenticated():
        messages.add_message(request,message.INFO,'Please Login')
        return redirect('/login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    
    username = request.session['username']
    
    if request.method == 'POST':
        
        form = CreateGameForm(request.POST)
        
        
        return render(request, 'statistics/leaderboard.html', {'form':form})
        
    else:

        return render(request, 'statistics/leaderboard.html', {'form':form})

def _getTopRanked(limit):
    """
    This method finds and retrieve's the top ranked users

    Keyword arguments:
    limit -- limit of how many top ranked users to get
    
    Contributors:
    Matthew Hengeveld
    
    Output:
    topRanked -- list of top ranked (in order)
    """
    topUsers = RankView.objects.all()[0:limit]
    
    topRanked = []
    
    for x in range(len(topUsers)):
        user_id = topUsers[x].id
        user = PongUser.objects.get(id=user_id)
        topRanked.append(user)
    
    return topRanked

def _getInstitutionRank(username):
    """
    This method finds and retrieve's a User's ranking within their own institution

    Keyword arguments:
    username -- the username of the user to find (string)
    
    Contributors:
    Quinton Black
    
    Output:
    rank -- the rank of the user at his or her institution (int)
    """
    user = PongUser.objects.get(username=username)
    institution = user.getInstitution()
    insitutionUsers = PongUser.objects.filter(_institution=institution).order_by('ranking')
    
    rank = 0    
    player = insitutionUsers[rank]
    number_players = len(insitutionUsers)
    while rank<number_players and player.username!=username:
        player = insitutionUsers[rank]
        rank+=1
        
    return rank+1

def _getOverallRank(username):
    """
    This method retireves a user's overall ranking

    Keyword arguments:
    username -- the username of the user to find (string)
    
    Contributors:
    Quinton Black
    
    Output:
    rank -- the rank of the user overall (int)
    """
    user = PongUser.objects.get(username=username)
    userId = user.getID()
    rankingTable = Ranking.objects.order_by('id')
    skillList = []
   
    for row in rankingTable:
        #please insert actual true skill calculation
        skill = row.mu - 3*row.sigma #<- here it is | Richard 
        skillList += {'userID':row.user_id,'skill':skill}
     
    
    skillList=sorted(skillList,key='rank')   
    
    overallRank = 0
    found = False
    while overallRank<len(skillList) and found==False:
        if skillList[overallRank]['userID']==userID:
            found = True
        overallRank+=1
    
    return overallRank    
    
def getInstitutionLeaders(numberOfLeaders, institutionName):
    """
    This method retrieves a list of length numberOfUsers of the top ranking users at institution specified
    Keyword arguments:
    numberOfUsers -- The number of users to return (int)
    intitutionName -- the name of the institution (String)
     
    Contributors:
    Matthew Hengeveld
    
    Output:
    2-demensional list of leaders -- [[leader1(PongUser), rank(int)], [leader2, rank]...]]
    """

    leaders = []
    count = 1
    querySize = 2000
    while len(leaders) < numberOfLeaders:
        min = (count-1)*querySize
        max = (count*querySize)-1
        userRanks = RankView.objects.all()[min:max]
        if (len(userRanks) < max):
            size = len(userRanks)
        else:
            size = querySize
        for x in range(size):
            user_id = userRanks[x].id
            user = PongUser.objects.get(id=user_id)
            userInstitution = user.getInstitution()
            if (userInstitution == institutionName):
                rank = x+((count-1)*querySize)
                leaders.append([user, rank+1])
        count += 1

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
    count = 1
    querySize = 1000
    user_id = user.id
    
    while rank == None:
        min = (count-1)*querySize
        max = (count*querySize)-1
        userRanks = RankView.objects.all()[min:max]
        if (len(userRanks) < max):
            size = len(userRanks)
        else:
            size = querySize
        for x in range(size):
            if (userRanks[x].id == user_id):
                rank = x+((count-1)*querySize)
        count += 1
    
    return rank + 1