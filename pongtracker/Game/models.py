from django.db import models
from User.models import User

class Team(models.Model):
    username1 = models.ForgeignKey(User)
    username2 = models.ForgeignKey(User)

class Game(models.Model):
    date_played = DateTimeField(auto_now=True)
    team1 = models.OneToOne(Team)
    team2 = models.OneToOne(Team)