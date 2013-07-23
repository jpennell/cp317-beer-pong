from django.db import models
from User.models import PongUser

# Create your models here.
class LifeStats(models.Model):
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    bounceShots = models.IntegerField(default=0)
    trickShots = models.IntegerField(default=0)
    partyFouls = models.IntegerField(default=0)
    redemptions = models.IntegerField(default=0)
    cup1Sunk = models.IntegerField(default=0)
    cup2Sunk = models.IntegerField(default=0)
    cup3Sunk = models.IntegerField(default=0)
    cup4Sunk = models.IntegerField(default=0)
    cup5Sunk = models.IntegerField(default=0)
    cup6Sunk = models.IntegerField(default=0)
    user = models.OneToOneField (PongUser)
      
    def __unicode__(self):
        return self.wins
    
class Ranking(models.Model):

    mu = models.FloatField(default=25.0)
    sigma = models.FloatField(default=8.3333)
    user = models.OneToOneField (PongUser)
    
    def _get_rank(self):
       "Returns the rank"
       return round(self.mu - (3*self.sigma),5)
   
    rank = property(_get_rank)
    
    def __unicode__(self):
        return self.rank
    
class RankView(models.Model):
    id = models.IntegerField(primary_key=True)
    skill_number = models.FloatField()
    
    class Meta:
        managed=False
        db_table='Statistics_rankView'
