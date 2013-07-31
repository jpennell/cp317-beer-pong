from Game.models import Game

def obtainGame(game_id):
    """
    Takes a game_id and find its corresponding Game.

    Keyword arguments:
    game_id -- a Game's id
    
    Contributors: Richard Douglas
    
    Output: the Game corresponding to the id or None if no such Game exists.
    """
    game = None
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        game = None
    return game

def isGameEnded(game):
    """
    Takes a Game object and determines if the Game has ended

    Keyword arguments:
    game -- the Game to check
    
    Contributors: Richard Douglas
    
    Output: True if the Game has ended, False otherwise
    """
    
    """REMOVE THIS LINE WHEN Score Game IS READY"""
    return True 
    
    events = game.getEvents()
    if events == []:
        ended = False
    else:
        lastEvent = events[-1]
        eventType = lastEvent.getEventType()
        ended = (eventType.getName() == "win")
    return ended

def isUserOnTeam(team, username):
    """
    Determines whether a PongUser is on this particular Team.
    
    Keyword arguments:
    team -- the Team we are checking
    username -- the username of the PongUser
    
    Contributors: Richard Douglas
    
    Output: True if the PongUser is on the Team, False otherwise.
    """
    teamUsers = [team.getUser1(), team.getUser2()]
    teamUsernames = [teamUser.getUsername() for teamUser in teamUsers]
    return username in teamUsernames

def isUserAllowedToVerifyGame(game,username):
    """
    Determines whether a PongUser is allowed to verify a particular Game.
    
    Keyword arguments:
    game -- the Game we are checking
    username -- the username of the PongUser
    
    Contributors: Richard Douglas
    
    Output: True if the PongUser is on the Team opposing the PongUser who created the Game, False otherwise.
    """
    return isUserOnTeam(game.getTeam2(),username) 

def obtainWinningTeamLosingTeam(game):
    """
    Takes a Game and returns the Team who won and the Team who lost.
    
    Keyword arguments:
    game -- the Game we are checking
    
    Contributors: Richard Douglas
    
    Output: winners -- the Team who won
            losers -- the Team who lost
            
            these are set to None if the Game has not ended
    """
    if (not isGameEnded(game)):
        winners = None
        losers = None
    else:
        endGameEvent = game.getEvents()[-1]
        teamCaptain = endGameEvent.getUser()
        if isUserOnTeam(game.getTeam1(),teamCaptain.username):
            winners = game.getTeam1()
            losers = game.getTeam2()
        else:
            winners = game.getTeam2()
            losers = game.getTeam1()
    return winners, losers
    
