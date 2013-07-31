from django import forms

class ConfirmGameForm(forms.Form):
    
    def setGameData(self, game):
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
        #lastly write the game_id so that the form knows which page to go to
        self.game_id = game.pk
        return