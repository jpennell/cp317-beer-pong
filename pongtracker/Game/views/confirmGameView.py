import TrueSkill

def confirmGameRequest(request):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    
    Output:
        
    """
    return 

def confrimOrDenyGame(gameID,isUserConfirming):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    
    Output:
        
    """
    obtainGame()
    isConfirmedOrDenied()
    isEnded()
    confirmGame()
    setConfirmedOrDenided()
    
    
    return 


def __confirmGame(game):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    
    Output:
        
    """
	#get Teams and Users
	team1 = game.getTeam1()
	team2 = game.getTeam2()
	users = [team1.getUser1(),team1.getUser2(),team2.getUser1(),team2.getUser2()]
    
	#get Events
	events = game.getEvents()
	cupEvents, endGameEvent = events[0:len(events) - 1],events[len(events) - 1]
	
	#process Events that involve cups being sunk
	for cupEvent in cupEvents:
		responsibleUser = cupEvent.getUser()
		index = __linearSearch(responsibleUser,users)
		stats = users[i].getLifeStats()
		__updateStatsWithEvent(stats,cupEvent)
		
	#process the end of the Game
	winningTeam, losingTeam = __obtainWinnersAndLosers(endGameEvent, team1, team2)
	__updateWinsAndLosses(winningTeam,losingTeam)
	__updateRankings(winningTeam,losingTeam)
    return
    
def __updateStatsWithEvent(stats,event):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    
    Output:
        
    """
	type = event.getEventType()
	if (type == "BOUNCE SHOT"):
		stats.incBounceShots(1)
	elif (type == "TRICK SHOT"):
		stats.incTrickShots(1)
	elif (type == "PARTY FOUL"):
		stats.incPartyFouls(1)
	elif (type == "CUP SUNK"):
		stats.incCupSunk(1)
	elif (type == "REDEMPTION"):
		stats.incRedemptions(1)
	return


def __updateWinsAndLosses(winningTeam,losingTeam):
    """updates the wins and losses of the Teams that played the Game

    Keyword arguments:
    winningTeam -- the Team that won the Game 
    losingTeam -- the Team that lost the Game 
    
    Contributors: Richard Douglas
    
    Output: 
        
    """
	#obtain the Users
	winningUsers = [winningTeam.getUser1(), winningTeam.getUser2()]
	losingUsers = [losingTeam.getUser1(), losingTeam.getUser2()]
	
	#update their wins/losses
	for winner in winningUsers:
		winner.getLifeStats().incWins(1)
	for loser in losingUsers:
		loser.getLifeStats().incLosses(1)
    return

def __updateRankings(winningTeam,losingTeam):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    
    Output:
        
    """
	#obtain the generic Ranking objects
	winningRankings = __obtainRankings(winningTeam)
	losingRankings = __obtainRankings(losingTeam)
	
	#obtain the corresponding TrueSkill Rating objects
	oldWinningRatings = __obtainRatings(winningRankings)
	oldLosingRatings = __obtainRatings(losingRankings)
	
	#have TrueSkill rate the Game
	newWinningRatings, newLosingRatings = TrueSkill.rate([oldWinningRatings,oldLosingRatings], ranks = [0,1])
	
	#update Ranking objects with their new Mu and Sigma values
	__writeRatingsToRankings(newWinningRatings,winningRankings)
	__writeRatingsToRankings(newLosingRatings,losingRankings)
    return
    
def __obtainWinnersAndLosers(endGameEvent,team1,team2):
    """helper function that takes a Game's Teams and ending Event
	and returns [winningTeam,losingTeam]

    Keyword arguments:
    endGameEvent -- the Event that ended the Game and knows who won 
    team1 -- the Game's Team1
	team2 -- the Game's Team2
    
    Contributors: Richard Douglas
    
    Output: victoryArray -- [winningTeam,losingTeam]
        
    """
	howItEnded = endGameEvent.getEventType()
	
	if (howItEnded == "TEAM1 WON"):
		victoryArray = [team1,team2]
	else:
		victoryArray = [team2, team1]
    return victoryArray
	
def __obtainRankings(team):
	users = [team.getUser1(), team.getUser2()]
	rankings = [users[0].getRanking(), users[1].getRanking()]
	return rankings

def __obtainRatings(rankings):
	ratings = []
	for ranking in rankings:
		mu = ranking.getMu()
		sigma = ranking.getSigma()
		rating = TrueSkill.Rating(mu,sigma)
		ratings.append(rating)
	return ratings
	
def __writeRatingsToRankings(ratings,rankings):
	for i in range(len(ratings)):
		mu = ratings[i].getMu()
		sigma = ratings[i].getSigma()
		rankings[i].setMu(mu)
		rankings[i].setSigma(sigma)
	return
	
def __linearSearch(value,array):
	i = 0
	while (i < len(array) and value != array[i]):
		i += 1
	if (i == len(array)):
		i = -1
	return i