# Create your views here.
from django.contrib.auth.models import User
from Game.models import Game, Team
from django.shortcuts import render, redirect

def createNewGameRequest(request):

    if request.method == 'POST':

        #form posted, where <input type="text", name="username1"></input>
        username1 = request.POST.get("username1")
        username2 = request.POST.get("username2")
        username3 = request.POST.get("username3")
        username4 = request.POST.get("username4")
        
        print("username1")

        game = _createNewGame(username1, username2, username3, username4)

        return redirect('/game/' + str(game.id))
    
    else:
        return render(request, 'game/create.html')


def _createNewGame(username1, username2, username3, username4):

    user1 = User.objects.get(username=username1)
    user2 = User.objects.get(username=username2)

    user3 = User.objects.get(username=username3)
    user4 = User.objects.get(username=username4)

    team1 = Team.objects.create(user1=user1,user2=user2)
    team2 = Team.objects.create(user1=user3,user2=user4)

    game = Game.objects.create(team1=team1, team2=team2)
    return game

def getGame(request,game_id):

    game = Game.objects.get(pk=game_id)

    return render(request, 'game/detail.html',{'game':game})
