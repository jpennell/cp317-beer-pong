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
    _deathCups = models.IntegerField(default=0)
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
    
    def getDeathCups(self):
        return self._deathCups
    
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
    
    def incWins(self, increment):
        self._wins += increment
    
    def incLoses(self, increment):
        self._loses += increment
    
    def incBounceShots(self, increment):
        self._bounceShots += increment
    
    def incTrickShots(self, increment):
        self._trickShots += increment
    
    def incPartyFouls(self, increment):
        self._partyFouls += increment
        
    def incRedemptions(self, increment):
        self._redemptions += increment
        
    def incDeathCups(self, increment):
        self._deathCups += increment
        
    def incCup1Sunk(self, increment):
        self._cup1Sunk += increment
        
    def incCup2Sunk(self, increment):
        self._cup2Sunk += increment
    
    def incCup3Sunk(self, increment):
        self._cup3Sunk += increment
        
    def incCup4Sunk(self, increment):
        self._cup4Sunk += increment
        
    def incCup5Sunk(self, increment):
        self._cup5Sunk += increment
        
    def incCup6Sunk(self, increment):
        self._cup6Sunk += increment
        
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
         
    def setDeathCups(self, value):
         self._deathCups= value
         
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
    
    
class RankView(models.Model):
    """ Rank view -- represents a View in the database
        ***VIEW MUST BE CREATED MANUALLY IN DATABASE USING FOLLOWING SCRIPT***
        
        CREATE 
            ALGORITHM = UNDEFINED 
            DEFINER = `pong`@`%` 
            SQL SECURITY DEFINER
        VIEW `pong`.`Statistics_rankView` AS
            select 
                `r`.`_user_id` AS `id`,
                round((`r`.`_mu` - (3 * `r`.`_sigma`)), 5) AS `_skillNumber`
            from
                `pong`.`Statistics_ranking` `r`
            order by (`r`.`_mu` - (3 * `r`.`_sigma`)) desc
    
    
        Keyword arguments:
        
        Contributors:
        Matt Hengeveld
        
        Output:
        
                
        """
    id = models.IntegerField(primary_key=True)
    _skillNumber = models.FloatField()
    user = models.OneToOneField (PongUser)
    
    class Meta:
        managed=False #tells django not to create this as a table when doing a syncdb
        db_table='Statistics_rankView' #tells django the name of the view
        
    def getSkillNumber(self):
        return self._skillNumber
