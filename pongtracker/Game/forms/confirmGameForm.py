from django import forms
from Utilities.game_utilities import obtainWinningTeam

class ConfirmGameForm(forms.Form):
    
    def setGameData(self, game):
        """
        Stores information about the Game in the form.
        This information can then be accessed by: 
        
        form.player1, ..., form.player4 -- the usernames of the PongUsers who played the Game
        form.date_played -- the date the Game was played
        form.game_id -- the number used to figure out where the Game is on the website
        form.outcome -- a String that is either "Team 1 Won" or "Team 2 Won" depending on how the Game ended
    
        Keyword arguments:
        game -- the Game whose information we want (game must have ended)
        
        Contributors: Richard Douglas
        
        Output: None
        """
        #obtain the usernames
        teams = [game.getTeam1(),game.getTeam2()]
        team1 = [teams[0].getUser1(),teams[0].getUser2()]
        team2 = [teams[1].getUser1(),teams[1].getUser2()]
        usernames = [team1[0].getUsername(), team1[1].getUsername(),
                     team2[0].getUsername(), team2[1].getUsername()]
        
        #store the usernames
        self.player1 = usernames[0]
        self.player2 = usernames[1]
        self.player3 = usernames[2]
        self.player4 = usernames[3]
        
        #also write the date to the form
        self.date_played = game.getDatePlayed()
        #write down who won
        self.outcome = self._obtainOutcomeOfEndedGame(game)
        #lastly write the game_id so that the form knows which page to go to
        self.game_id = game.pk
        return
    
    def _obtainOutcomeOfEndedGame(self, game):
        """
        Determines whether the form's outcome attribute should be "Team 1 Won" or "Team 2 Won"
        when a Game's information is being written to it.
    
        Keyword arguments:
        game -- the Game whose information is being written to the form (game must have ended) 
        
        Contributors: Richard Douglas
        
        Output: outcome, a String that is "Team 1 Won" if Team 1 won the Game
                         and "Team 2 Won" otherwise.
        """
        winningTeam = obtainWinningTeam(game)
        if winningTeam == game.getTeam1():
            outcome = "Team 1 Won"
        else:
            outcome = "Team 2 Won"
        return outcome