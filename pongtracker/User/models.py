from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
import datetime
from django.contrib.contenttypes.models import ContentType



class Institution(models.Model):
    def getName(self):
        return self._name
    
    _name = models.CharField(max_length=45)

    def __unicode__(self):
        return self._name
    
class PongUser(AbstractUser):
        
    def getUsername(self):
        return self.username    
        
    def getHeight(self):
        return self._height

    def getID(self):
        return self.id
    
    def getPhoto(self):
        return self._photo

    def getGraduationYear(self):
        return self._graduationYear

    def getInstitution(self):
        return self._institution

    def getIsBanned(self):
        return self._isBanned
    
    def getIsActive(self):
        return self.is_active
    
    def getFirstName(self):
        return self.first_name
    
    def getLastName(self):
        return self.last_name
    
    def getEmail(self):
        return self._email
    
    def getHasUpdatedProfile(self):
        return self._hasUpdatedProfile
    
    def getLifeStats(self):
        return self.lifestats
    
    def getHasAcceptedTerms(self):
        return self._hasAcceptedTerms    
    
    def getConfirmRequired(self):
        return self._confirmRequired
    
    def getRanking(self):
        return self.ranking


    def setHeight(self, value):
        self._height = value

    def setPhoto(self, value):
        self._photo = value

    def setGraduationYear (self, value):
        self._graduationYear = value

    def setInstitution(self, value):
        self._institution = value

    def setIsBanned(self, value):
        self._isBanned = value
        
    def setIsActive(self, value):
        self.is_active = value
    
    def setFirstName(self, value):
        self.first_name = value
    
    def setLastName(self, value):
        self.last_name = value
    
    def setEmail(self, value):
        self.email = value
        
    def setHasUpdatedProfile(self, value):
        self._hasUpdatedProfile = value
        
    def setHasAcceptedTerms(self, value):
        self._hasAcceptedTerms = value    
    
    def setConfirmRequired(self, value):
        self._confirmRequired = value    
        
    YEAR_CHOICES = []

    for r in range((datetime.datetime.now().year),(datetime.datetime.now().year+6)):
        YEAR_CHOICES.append((r,r))
        
    _height = models.SmallIntegerField(null = True, blank = True,help_text="cm")
    _photo = models.ImageField(upload_to="profile_photo",blank=True,null=True)
    _graduationYear = models.IntegerField(('year'), max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year+1)
    _institution = models.ForeignKey(Institution,null = True, blank = True)
    _isBanned = models.BooleanField(default=False)
    _hasUpdatedProfile = models.BooleanField(default = False)
    #_hasAcceptedTerms =  models.BooleanField(default = False)
    _confirmRequired =  models.BooleanField(default = False)
    
