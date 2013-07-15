from django.db import models
from User.models import PongUser

class Team(models.Model):
    user1 = models.ForeignKey(PongUser,related_name="Team1")
    user2 = models.ForeignKey(PongUser,related_name="Team2")

class Game(models.Model):
    date_played = models.DateTimeField(auto_now=True)
    team1 = models.OneToOneField(Team,related_name="Game1")
    team2 = models.OneToOneField(Team,related_name="Game2")

    def get_team1():
        return self.team1

    def get_team2():
        return self.team2

    def get_date_played():
        return self.date_played

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
    user = models.ForeignKey(PongUser, related_name = "Events")
