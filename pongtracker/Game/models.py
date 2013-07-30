from django.db import models
from User.models import PongUser

class Team(models.Model):
    _user1 = models.ForeignKey(PongUser,related_name="Team1")
    _user2 = models.ForeignKey(PongUser,related_name="Team2")
    
    def getUser1(self):
        return self._user1
    
    def getUser2(self):
        return self._user2
    
    def getUser(self, user_number):
        
        if user_number == 1:
            
            return self._user1
        
        elif user_number == 2:
            
            return self._user2
        
        else:
            
            return None
    
    def setUser1(self):
        self._user1 = value
    
    def setUser2(self,value):
        self._user2 = value
        

class Game(models.Model):
    _datePlayed = models.DateTimeField(auto_now=True)
    _team1 = models.OneToOneField(Team,related_name="Game1")
    _team2 = models.OneToOneField(Team,related_name="Game2")
    _isConfirmed = models.BooleanField(default = False)

    def getTeam1(self):
        return self._team1

    def getTeam2(self):
        return self._team2
    
    def getTeam(self, team_number):
        
        if team_number == 1:
            
            return self._team1
        
        elif team_number == 2:
            
            return self._team2
        
        else:
            
            return None

    def getDatePlayed(self):
        return self._datePlayed
    
    def getIsConfirmed(self):
        return self._isConfirmed
    
    def getEvents(self):
        return self.Events.all().order_by('_eventTime')
    
    def setIsConfirmed(self, value):
        self._isConfirmed = value
        
    def setTeam1(self, value):
        self._team1 = value
        
    def setTeam2(self, value):
        self._team2 = value
        

class EventType(models.Model):
    _typeName = models.CharField(max_length=20)
    
    def getName(self):
        return self._typeName

    def __unicode__(self):
        return self._typeName

class Event(models.Model):
    _eventTime = models.DateTimeField(auto_now=True)
    _cup1 = models.BooleanField(default=False)
    _cup2 = models.BooleanField(default=False)
    _cup3 = models.BooleanField(default=False)
    _cup4 = models.BooleanField(default=False)
    _cup5 = models.BooleanField(default=False)
    _cup6 = models.BooleanField(default=False)
    _eventType = models.ForeignKey(EventType)
    _game = models.ForeignKey(Game,related_name = "Events")
    _user = models.ForeignKey(PongUser, related_name = "Events")
    
    def getEventTime(self):
        return self._eventTime
    
    def getCup1(self):
        return self._cup1
    
    def getCup2(self):
        return self._cup2
    
    def getCup3(self):
        return self._cup3
    
    def getCup4(self):
        return self._cup4
    
    def getCup5(self):
        return self._cup5
    
    def getCup6(self):
        return self._cup6
    
    def getEventType(self):
        return self._eventType
    
    def getGame(self):
        return self._game
    
    def getUser(self):
        return self._user
