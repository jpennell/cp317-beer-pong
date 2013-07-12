# Create your views here.
from django.contrib.auth.models import User
from Game.models import Game, Team
from django.shortcuts import render, redirect
from Utilities.views import *

def createNewGameRequest(request):

    if request.method == 'POST':
        
        errFlag = 0

        #form posted, where <input type="text", name="username1"></input>
        usernames = [request.POST.get("username1"), request.POST.get("username2"), request.POST.get("username3"), request.POST.get("username4")]
        
        #check for duplicate usernames
        for x in range(3):
            if (usernames.count(usernames[x]) > 1):
                errFlag = 1
        
        print(errFlag)
        
        if (errFlag == 1):     #duplicate users entered
            return render(request, 'game/create.html',{'errFlag':errFlag})
        
        users = [_findUser(usernames[0]), _findUser(usernames[1]), _findUser(usernames[2]), _findUser(usernames[3])]
        
        #check for users that don't exist      
        for x in range(4):
            if users[x] is None:
                errFlag = 2
        
        print(errFlag)
                
        if (errFlag == 0):  #no error; create game
            game = _createNewGame(users[0], users[1], users[2], users[3])
            
            return redirect('/game/' + str(game.id))
            
        elif (errFlag == 2):     #one or more users entered don't exist
            return render(request, 'game/create.html',{'errFlag':errFlag})
         
        else:
            return render(request, 'game/create.html',{'errFlag':errFlag})
    
    else:
        
        return render(request, 'game/create.html')


def _createNewGame(user1, user2, user3, user4):

    team1 = Team.objects.create(user1=user1,user2=user2)
    team2 = Team.objects.create(user1=user3,user2=user4)

    game = Game.objects.create(team1=team1, team2=team2)
    return game

def getGame(request,game_id):

    game = Game.objects.get(pk=game_id)
    
    print(game.team1.user1)

    return render(request, 'game/detail.html',{'game':game})

#finds user in the database; returns None is not found
def _findUser(username):
    user = None
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    finally:
        return user
