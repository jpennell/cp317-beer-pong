# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from Game.models import Game, Team
from django.shortcuts import render, redirect
from Utilities.utilities import *
from Game.forms.createGameForm import CreateGameForm
from django.template import Context

def createNewGameRequest(request):
    """validates input; creates a new game based on valid input

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors: Matt Hengeveld
    
    Output:
        
    """
    
    form = CreateGameForm()
    
    username = request.session['username']
    
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
            
            regUser = [request.POST.get("chkRegister2"), request.POST.get("chkRegister3"), request.POST.get("chkRegister4")]      
            usernames = [username, username2, username3, username4]
            emails = [email2, email3, email4]

            errFlag = False
            
            # check for duplicate usernames
            errFlag, index = _chkDup(usernames)
            
            # duplicate users entered        
            if (errFlag):
                form.error = "Duplicate user"
                form.errorIndex = index
                return render(request, 'game/create.html', {'form': form})
            
            # get users from database
            users = [_findUser(usernames[0]), _findUser(usernames[1]), _findUser(usernames[2]), _findUser(usernames[3])]     
            
            print("users: ", users)
            
            errFlag, index = _chkUsersExist(users[1:4], regUser)
            
            # one or more users entered don't exist    
            if (errFlag):
                form.error = "User not registered"
                form.errorIndex = index
                return render(request, 'game/create.html', {'form': form})
            
            #--------------------------------------------------------------------------
            # no errors; create game
            #--------------------------------------------------------------------------      
            game = _createNewGame(users[0], users[1], users[2], users[3])
            
            return redirect('/game/' + str(game.id))
            
        else:
            
            form = CreateGameForm()
            print("Invalid")
            return render(request, 'game/create.html', {'form': form})
         
#            #--------------------------------------------------------------------------
#            # get POSTed data
#            #--------------------------------------------------------------------------
#            regUser = [request.POST.get("chkRegister2"), request.POST.get("chkRegister3"), request.POST.get("chkRegister4")]      
#            usernames = [username, username2, username3, username4]
#            emails = [email2, email3, email4]
#            
#            print("usernames: ",username,username2,username3,username4)
#            
#            # check for blank usernames
#            errFlag = _chkBlank(usernames)
#            
#            # there was a blank username
#            if (errFlag):
#                print("Blank username")
#                form.error = "Please fill in all usernames."
#                return render(request, 'game/create.html', {'form': form})
#            
#            # check for duplicate usernames
#            errFlag = _chkDup(usernames)
#            
#            # duplicate users entered        
#            if (errFlag):    
#                print("Duplicates")
#                form.error = "Duplicate usernames are not allowed."
#                return render(request, 'game/create.html', {'form': form})
#                
#            # get users from database
#            users = [_findUser(usernames[0]), _findUser(usernames[1]), _findUser(usernames[2]), _findUser(usernames[3])]
#            
#            print(users)
#            
#            errFlag, index = _chkUsersExist(users, regUser)
#            
#            print(index)
#            
#            # one or more users entered don't exist    
#            if (errFlag):  
#                print("User does not exist")  
#                nullUserMess = ''
#                for i in index:
#                    nullUserMess += usernames[i]
#                print(nullUserMess)
#                form.error = "The following are not registered users on Pong Tracker: " + nullUserMess
#                return render(request, 'game/create.html', {'form': form})
#            
#            # register users not already registered
#            _regUsers(regUser, usernames, emails)       
#            
#            #--------------------------------------------------------------------------
#            # no errors; create game
#            #--------------------------------------------------------------------------      
#            game = _createNewGame(users[0], users[1], users[2], users[3])
#            
#            return redirect('/game/' + str(game.id))
#        
#        else:
#            form = CreateGameForm()
#            print("Invalid")
#            return render(request, 'game/create.html', {'form': form})
#        
#    else:
#        return render(request, 'game/create.html',{'form': form})


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
        user = get_user_model().objects.get(username=username)
    except User.DoesNotExist:
        user = None
    finally:
        return user
    

def _chkBlank(usernames):
    """checks for blank usernames

    Keyword arguments:
    usernames -- list of strings; usernames entered on form
    
    Contributors: Matt Hengeveld
    
    Output:     False if no duplicates
                True if duplicates
        
    """
    
    errFlag = False;
    
    for x in range(len(usernames)):
        if usernames[x] == '':
             errFlag = True
             
    return errFlag
    

def _chkDup(usernames):
    """checks for duplicate usernames

    Keyword arguments:
    usernames -- list of strings; usernames entered on form
    
    Contributors: Matt Hengeveld
    
    Output:     False if no duplicates
                True if duplicates
        
    """
    
    errFlag = False;
    index = []
    
    for x in range(len(usernames)):
        if (usernames.count(usernames[x]) > 1):
            errFlag = True
            index.append(x+1)
                
    return errFlag, index


def _chkUsersExist(users, regUser):
    """checks database to see if users exist; does not check users that have 'register to play' checked

    Keyword arguments:
    users -- list of users
    regUser -- list of checkbox states (indicating 'register to play')
    
    Contributors: Matt Hengeveld
    
    Output:     False if a user does not exist
                True if all users exist
                index contains index of user(s) that does not exist
        
    """
    
    errFlag = False
    index = []

    for x in range(len(users)):
        if regUser[x] is None:
            if users[x] is None:
                errFlag = True
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
    
    for x in usernames:
        if regUser[x] is not None:
            user = _findUser(usernames[x])
            print(usernames + "/" + user + "/" + regUser)
            if user is None:
                rndPassword = createRndPass(8)
                User.objects.create_user(username=usernames[x],emails=email[x],password=rndPassword)
                print(rndPassword)
    
    return