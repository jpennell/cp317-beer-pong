from django.db import models
from User.models import PongUser


# Create your models here.
class LifeStats(models.Model):
    _wins = models.IntegerField(default=0)
    _loses = models.IntegerField(default=0)
    _bounceShots = models.IntegerField(default=0)
    _trickShots = models.IntegerField(default=0)
    _partyFouls = models.IntegerField(default=0)
    _redemptions = models.IntegerField(default=0)
    _cup1Sunk = models.IntegerField(default=0)
    _cup2Sunk = models.IntegerField(default=0)
    _cup3Sunk = models.IntegerField(default=0)
    _cup4Sunk = models.IntegerField(default=0)
    _cup5Sunk = models.IntegerField(default=0)
    _cup6Sunk = models.IntegerField(default=0)
    _user = models.OneToOneField (PongUser)
    
    def getWins(self):
        return self._wins
    
    def getLoses(self):
        return self._loses
    
    def getBounceShots(self):
        return self._bounceShots
    
    def getTrickShots(self):
        return self._trickShots
    
    def getPartyFouls(self):
        return self._partyFouls
    
    def getRedemptions(self):
        return self._redemptions
    
    def getCup1Sunk(self):
        return self._cup1Sunk
    
    def getCup2Sunk(self):
        return self._cup2Sunk
    
    def getCup3Sunk(self):
        return self._cup3Sunk
    
    def getCup4Sunk(self):
        return self._cup4Sunk
    
    def getCup5Sunk(self):
        return self._cup5Sunk
    
    def getCup6Sunk(self):
        return self._cup6Sunk
    
    def setWins(self, value):
         self._wins = value
    
    def setLoses(self, value):
         self._loses= value
    
    def setBounceShots(self, value):
         self._bounceShots= value
    
    def setTrickShots(self, value):
         self._trickShots= value
    
    def setPartyFouls(self, value):
         self._partyFouls= value
    
    def setRedemptions(self, value):
         self._redemptions= value
    
    def setCup1Sunk(self, value):
         self._cup1Sunk= value
    
    def setCup2Sunk(self, value):
         self._cup2Sunk= value
    
    def setCup3Sunk(self, value):
         self._cup3Sunk= value
    
    def setCup4Sunk(self, value):
         self._cup4Sunk= value
    
    def setCup5Sunk(self, value):
         self._cup5Sunk= value
    
    def setCup6Sunk(self, value):
         self._cup6Sunk= value
    
    def __unicode__(self):
        return self._wins
    
class Ranking(models.Model):

    _mu = models.FloatField(default=25.0)
    _sigma = models.FloatField(default=8.3333)
    _user = models.OneToOneField (PongUser)
    
    def setMu(self, value):
        self._mu = value
        
    def setSigma(self, value):
        self._sigma = value
        
    def getMu(self):
        return self._mu
    
    def getSigma(self):
        return self._sigma
    
    def _getRank(self):
       "Returns the rank"
       return round(self.mu - (3*self.sigma),5)
   
    _rank = property(_getRank)
    
    def __unicode__(self):
        return self._rank
    
class RankView(models.Model):
    id = models.IntegerField(primary_key=True)
    _skillNumber = models.FloatField()
    
    class Meta:
        managed=False
        db_table='Statistics_rankView'
        
    def getSkillNumber(self):
        return self._skillNumber
