from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from Game.models import Game, Team
from django.shortcuts import render, redirect
from Utilities.utilities import *
from Game.forms.createGameForm import CreateGameForm
from django.template import Context
from User.views.registrationView import *
from django.contrib import messages

def createNewGameRequest(request):
    """validates input; creates a new game based on valid input

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors: Matt Hengeveld
    
    Output:
            
    """
    if not request.user.is_authenticated():
        messages.add_message(request,messages.INFO,'Please Login')
        return redirect('/login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    
    username = request.session['username']
    
    form = CreateGameForm(initial={'username1':username})
    # on POST
    if request.method == 'POST':
        form = CreateGameForm(request.POST)

        if form.is_valid():
            
            # clean all data
            username2 = form.cleaned_data['username2']
            username3 = form.cleaned_data['username3']
            username4 = form.cleaned_data['username4']
            
            email2 = form.cleaned_data['email2']
            email3 = form.cleaned_data['email3']
            email4 = form.cleaned_data['email4']
            
            chkRegister2 = form.cleaned_data['chkRegister2']
            chkRegister3 = form.cleaned_data['chkRegister3']
            chkRegister4 = form.cleaned_data['chkRegister4']
    
            # put all data in lists
            regUser = [False,chkRegister2, chkRegister3, chkRegister4]      
            usernames = [username, username2, username3, username4]
            emails = ['', email2, email3, email4]

            
            #CHECK TO SEE IF ANY USERNAMES ARE TAKEN AND SUGGESTIONS ARE NEEDED
            suggestionList=_getUsernameTakenSuggestions(usernames, regUser)
            if suggestionList.count([''])<4:
                if suggestionList[1]!=['']:
                    form.suggestedUsernames2 = suggestionList[1]
                if suggestionList[2]!=['']:              
                    form.suggestedUsernames3 = suggestionList[2]
                if suggestionList[3]!=['']:                
                    form.suggestedUsernames4 = suggestionList[3]
                                
            else:
                # register users
                users = _regUsers( usernames, emails, regUser) 
                
                # no errors; create game     
                game = _createNewGame(users[0], users[1], users[2], users[3])
                
                return redirect('/game/' + str(game.id) +'/play')
            
        else:

            return render(request, 'game/create.html', {'form': form})      

    context = Context({'title': 'Create Game', 'form': form, 'username':username})
           
    return render(request, 'game/create.html',context)

def _getUsernameTakenSuggestions(usernames,regUser):
    
    suggestionList=[]
    x = 0
    for username in usernames:
        if regUser[x] is True:
            user = _findUser(username)
            if user is not None:
                suggestionForUser =suggestUsernames(username, 5)
                suggestionList.append(suggestionForUser)
            else:
                suggestionList.append([''])
        else:
            suggestionList.append([''])
        x+=1
    
    return suggestionList
                


def _createNewGame(user1, user2, user3, user4):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    
    Output:
        
    """

    team1 = Team.objects.create(_user1=user1,_user2=user2)
    team2 = Team.objects.create(_user1=user3,_user2=user4)

    game = Game.objects.create(_team1=team1, _team2=team2)
    
    return game

def getGame(request,game_id):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    
    Output:
        
    """
    game = Game.objects.get(pk=game_id)
    
    return render(request, 'game/detail.html',{'game':game})


def _findUser(username):
    """finds user in the database

    Keyword arguments:
    username -- string; username entered on form
    
    Contributors: Matt Hengeveld
    
    Output:    user object; returns None is not found
        
    """
    user = None
    try:
        user = PongUser.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    finally:
        return user   


def _chkRegUsers(users, regUser):
    
    for x in range(len(users)):
        if regUser[x] is not None:
            if users[x] is not None:
                errList[x+1] = "Username taken\nSuggestions:\n"
                suggestions = suggestUsernames(users[x].username, 4)
                for n in range(len(suggestions)):
                    errList[x+1] += (suggestions[n] + "\n")
             
    return errList



def _regUsers( usernames, emails, regUser):
    """registers users who aren't already registered; assigns 8 character random password; emails username and password

    Keyword arguments:
    regUser -- list of checkbox states (indicating 'register to play')
    usernames -- list of usernames
    emails -- list of emails to register with
    
    Contributors: Matt Hengeveld
    
    Output:     nothing
        
    """   
    users=[]
    for x in range(len(usernames)):
        if regUser[x] is not False:
            regGameUser(usernames[x], emails[x])
        users.append( _findUser(usernames[x]))
    
    return users