from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    user1 = models.ForeignKey(User,related_name="User1")
    user2 = models.ForeignKey(User,related_name="User2")

class Game(models.Model):
    date_played = models.DateTimeField(auto_now=True)
    team1 = models.OneToOneField(Team,related_name="Team1")
    team2 = models.OneToOneField(Team,related_name="Team2")

class Event(models.Model):
    event_time = models.DateTimeField(auto_now=True)
    cup1 = models.Boolean(default=False)
    cup2 = models.Boolean(default=False)
    cup3 = models.Boolean(default=False)
    cup4 = models.Boolean(default=False)
    cup5 = models.Boolean(default=False)
    cup6 = models.Boolean(default=False)
    event_type = models.ForeignKey(EventType)
      
class EventType(models.Model):
    typeName = models.CharField(max_length=20)