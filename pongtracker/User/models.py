from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class Institution(models.Model):
    name = models.CharField(max_length=45)

    def __unicode__(self):
        return self.name
    
class PongUser(AbstractUser):
    
    YEAR_CHOICES = []
    for r in range((datetime.datetime.now().year),(datetime.datetime.now().year+10)):
        YEAR_CHOICES.append((r,r))
        
    height = models.SmallIntegerField(null = True, blank = True)
    photo = models.CharField(max_length=100, null = True, blank = True)
    graduation_year = models.IntegerField(('year'), max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year+1)
    institution = models.ForeignKey(Institution,null = True, blank = True)
    is_banned = models.BooleanField(default=False)
    
