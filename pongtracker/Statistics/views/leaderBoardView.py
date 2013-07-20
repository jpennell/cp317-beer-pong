from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from User.models import PongUser
from User.models import Institution
from Statistics.models import LifeStats, Ranking


def leaderboardPage(request):
    if not request.user.is_authenticated():
         return redirect('/login/')
    
    topTen = PongUser.objects.order_by('ranking')[0:10]
    username = request.session['username']  
    institutionRank =_getInstitutionRank(username)
    overallRank = _getOverallRank(username)
    print('Institution Rank:{0}'.format(institutionRank))
    print('Overall Rank:{0}'.format(overallRank))
    
    return render(request,'statistics/leaderboard.html',{'username':request.session['username']})

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
    
def _getLeaders(numberOfUsers,i):
    """
    This method retireves a user's overall ranking

    Keyword arguments:
    username -- the username of the user to find (string)
    
    Contributors:
    Quinton Black
    
    Output:
    rank -- the rank of the user overall (int)
    """
    
    