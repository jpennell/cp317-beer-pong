from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    user1 = models.ForeignKey(User,related_name="Teams1")
    user2 = models.ForeignKey(User,related_name="Teams2")

class Game(models.Model):
    date_played = models.DateTimeField(auto_now=True)
    team1 = models.OneToOneField(Team,related_name="Game1")
    team2 = models.OneToOneField(Team,related_name="Game2")
    
class EventType(models.Model):
    typeName = models.CharField(max_length=20)
    

class Event(models.Model):
    event_time = models.DateTimeField(auto_now=True)
    cup1 = models.BooleanField(default=False)
    cup2 = models.BooleanField(default=False)
    cup3 = models.BooleanField(default=False)
    cup4 = models.BooleanField(default=False)
    cup5 = models.BooleanField(default=False)
    cup6 = models.BooleanField(default=False)
    event_type = models.ForeignKey(EventType)
    game = models.ForeignKey(Game,related_name = "Events")
    user = models.ForeignKey(User, related_name = "Events")