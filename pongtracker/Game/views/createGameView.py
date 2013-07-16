# Create your views here.
from django.contrib.auth.models import User
from Game.models import Game, Team
from django.shortcuts import render, redirect
from Utilities.views import *

def createNewGameRequest(request):
    """validates input; creates a new game based on valid input

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors: Matt Hengeveld
    
    Output:
        
    """
    
    if 'username' in request.session:
        username = request.session['username']
        print (username)
        return render(request, 'game/create.html',{'username':username})
    
    if request.method == 'POST':
        
        errFlag = 0
        
        #--------------------------------------------------------------------------
        # get POSTed data
        #--------------------------------------------------------------------------
        usernames = [username, request.POST.get("username2"), request.POST.get("username3"), request.POST.get("username4")]
        regUser = [request.POST.get("chkRegister2"), request.POST.get("chkRegister3"), request.POST.get("chkRegister4")]
        emails = [request.POST.get("email2"), request.POST.get("email3"), request.POST.get("email4")]
        
        # check for duplicate usernames
        errFlag = _chkDup(usernames)
        
        # duplicate users entered        
        if (errFlag == 1):     
            return render(request, 'game/create.html',
                          {'errFlag':errFlag,
                           'username':usernames[0],
                           'username2':usernames[1],
                           'username3':usernames[2],
                           'username4':usernames[3]})
            
        # get users from database
        users = [_findUser(usernames[0]), _findUser(usernames[1]), _findUser(usernames[2]), _findUser(usernames[3])]
        
        errFlag, index = _chkUsersExist(users)
        
        # one or more users entered don't exist    
        if (errFlag == 1):     
            return render(request, 'game/create.html',{'errFlag':errFlag})
        
        # register users not already registered
        _regUsers(regUser, usernames, emails)       
        
        #--------------------------------------------------------------------------
        # no errors; create game
        #--------------------------------------------------------------------------      
        if (errFlag == 0):
            game = _createNewGame(users[0], users[1], users[2], users[3])
            
            return redirect('/game/' + str(game.id))
        else:
            return render(request, 'game/create.html')


def _createNewGame(user1, user2, user3, user4):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    
    Output:
        
    """

    team1 = Team.objects.create(user1=user1,user2=user2)
    team2 = Team.objects.create(user1=user3,user2=user4)

    game = Game.objects.create(team1=team1, team2=team2)
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
    
    print(game.team1.user1)

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
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    finally:
        return user


def _chkDup(usernames):
    """checks for duplicate usernames

    Keyword arguments:
    usernames -- list of strings; usernames entered on form
    
    Contributors: Matt Hengeveld
    
    Output:     0 if no duplicates
                1 if duplicates
        
    """
    
    errFlag = 0;
    
    for x in range(3):
        if (usernames.count(usernames[x]) > 1):
            errFlag = 1
                
    return errFlag


def _chkUsersExist(users, regUser):
    """checks database to see if users exist; does not check users that have 'register to play' checked

    Keyword arguments:
    users -- list of users
    regUser -- list of checkbox states (indicating 'register to play')
    
    Contributors: Matt Hengeveld
    
    Output:     0 if a user does not exist
                1 if all users exist
                index contains index of user(s) that does not exist
        
    """
    
    errFlag = 0;
    index = None;
   
    for x in range(3):
        if regUser[x] is None:
            if users[x+1] is None:
                errFlag = 1
                index.append(x+1)
    
    return errFlag, index

def _regUsers(regUser, usernames, emails):
    """registers users who aren't already registered; assigns 8 character random password; emails username and password

    Keyword arguments:
    regUser -- list of checkbox states (indicating 'register to play')
    usernames -- list of usernames
    emails -- list of emails to register with
    
    Contributors: Matt Hengeveld
    
    Output:     nothing
        
    """
    
    for x in range(usernames):
        if regUser[x] is not None:
            user = _findUser(usernames[x])
            print(usernames + "/" + user + "/" + regUser)
            if user is None:
                rndPassword = Utilities.createRndPass(8)
                User.objects.create_user(username=usernames[x],emails=email[x],password=rndPassword)
                print(rndPassword)
    
    return