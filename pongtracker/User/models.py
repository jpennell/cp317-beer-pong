from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class Institution(models.Model):
    name = models.CharField(max_length=45)

    def __unicode__(self):
        return self.name
    
class PongUser(AbstractUser):
    
    def getHeight(self):
        return self.height


    def getPhoto(self):
        return self.photo


    def getGraduationYear(self):
        return self.graduation_year


    def getInstitution(self):
        return self.institution


    def getIsBanned(self):
        return self.is_banned


    def setHeight(self, value):
        self.height = value


    def setPhoto(self, value):
        self.photo = value


    def setGraduationYear (self, value):
        self.graduation_year = value


    def setInstitution(self, value):
        self.institution = value


    def setIsBanned(self, value):
        self.is_banned = value
        
    def setIsactive(self, value):
        self.is_active = value
    
    def setFirstName(self, value):
        self.first_name = value
    
    def setLastName(self, value):
        self.last_name = value
    
    def setEmail(self, value):
        self.email = value
    
    
    YEAR_CHOICES = []
    for r in range((datetime.datetime.now().year),(datetime.datetime.now().year+10)):
        YEAR_CHOICES.append((r,r))
        
    height = models.SmallIntegerField(null = True, blank = True)
    photo = models.CharField(max_length=100, null = True, blank = True)
    graduation_year = models.IntegerField(('year'), max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year+1)
    institution = models.ForeignKey(Institution,null = True, blank = True)
    is_banned = models.BooleanField(default=False)
