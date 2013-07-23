from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class Institution(models.Model):
    def getName(self):
        return self._name
    
    _name = models.CharField(max_length=45)

    def __unicode__(self):
        return self._name
    
class PongUser(AbstractUser):
    
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
    
    def getHasLoggedIn(self):
        return self._hasLoggedIn


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
        self._is_active = value
    
    def setFirstName(self, value):
        self.first_name = value
    
    def setLastName(self, value):
        self.last_name = value
    
    def setEmail(self, value):
        self.email = value
        
    def setHasLoggedIn(self, value):
        self._hasLoggedIn = value
    
    
    YEAR_CHOICES = []
    for r in range((datetime.datetime.now().year),(datetime.datetime.now().year+10)):
        YEAR_CHOICES.append((r,r))
        
    _height = models.SmallIntegerField(null = True, blank = True)
    _photo = models.CharField(max_length=100, null = True, blank = True)
    _graduationYear = models.IntegerField(('year'), max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year+1)
    _institution = models.ForeignKey(Institution,null = True, blank = True)
    _isBanned = models.BooleanField(default=False)
    _hasLoggedIn = models.BooleanField(default = False)
