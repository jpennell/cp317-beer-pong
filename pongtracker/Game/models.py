from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    user1 = models.ForeignKey(User,related_name="User1")
    user2 = models.ForeignKey(User,related_name="User2")

class Game(models.Model):
    date_played = models.DateTimeField(auto_now=True)
    team1 = models.OneToOneField(Team,related_name="Team1")
    team2 = models.OneToOneField(Team,related_name="Team2")