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
            
            # put all data in lists
            regUser = [request.POST.get("chkRegister2"), request.POST.get("chkRegister3"), request.POST.get("chkRegister4")]      
            usernames = [username, username2, username3, username4]
            emails = [email2, email3, email4]

            # initialize error list
            errList = ['','','','']
            
            # check for duplicate usernames
            errList = _chkDup(usernames, errList)

            # get users from database
            users = [_findUser(usernames[0]), _findUser(usernames[1]), _findUser(usernames[2]), _findUser(usernames[3])]     
            
            # check if all users exist
            errList = _chkUsersExist(users[1:4], regUser, errList)
            
            errList = _chkEmails(regUser, emails, errList)
            
            # check if registering users have entered a taken username
            errList = _chkRegUsers(users[1:4], regUser, errList)
            
            # display errors in form
            if (errList.count('') < 4):
                form.err2 = errList[1]
                form.err3 = errList[2]
                form.err4 = errList[3]
                return render(request, 'game/create.html', {'form': form})  
            
            # no errors; create game     
            game = _createNewGame(users[0], users[1], users[2], users[3])
            
            return redirect('/game/' + str(game.id))
            
        else:
            # form is invalid
            _invalidErrors(form)
            return render(request, 'game/create.html', {'form': form})      
        
    else:
        return render(request, 'game/create.html',{'form': form})



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

def _invalidErrors(form):
    formErrors = []
    
    for error in form.errors:
        formErrors.append(error)
    
    if ('email2' in formErrors):
        form.err2 = "Invalid email"
    if ('email3' in formErrors):
        form.err3 = "Invalid email"
    if ('email4' in formErrors):
        form.err4 = "Invalid email"
    if ('username2' in formErrors):
        form.err2 = "This field is required"
    if ('username3' in formErrors):
        form.err3 = "This field is required"
    if ('username4' in formErrors):
        form.err4 = "This field is required"
    
    return

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

def _chkDup(usernames, errList):
    """checks for duplicate usernames

    Keyword arguments:
    usernames -- list of strings; usernames entered on form
    
    Contributors: Matt Hengeveld
    
    Output:     False if no duplicates
                True if duplicates
        
    """
    
    for x in range(len(usernames)):
        if (usernames.count(usernames[x]) > 1):
            errList[x] = "Duplicate user"
                
    return errList

def _chkUsersExist(users, regUser, errList):
    """checks database to see if users exist; does not check users that have 'register to play' checked

    Keyword arguments:
    users -- list of users
    regUser -- list of checkbox states (indicating 'register to play')
    
    Contributors: Matt Hengeveld
    
    Output:     False if a user does not exist
                True if all users exist
                index contains index of user(s) that does not exist
        
    """

    for x in range(len(users)):
        if regUser[x] is None:
            if users[x] is None:
                errList[x+1] = "User not registered"
    
    return errList

def _chkRegUsers(users, regUser, errList):
    
    for x in range(len(users)):
        if regUser[x] is not None:
            if users[x] is not None:
                errList[x+1] = "Username taken"
    
    return errList

def _chkEmails(regUser, emails, errList):
    
    print(emails)
    
    for x in range(len(regUser)):
        if regUser[x] is not None:
            if emails[x] is u'':
                errList[x+1] = "Email required for registration"
    
    return errList

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