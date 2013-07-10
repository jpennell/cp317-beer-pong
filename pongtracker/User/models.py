from django.db import models
from django.contrib.auth.models import User

class Institution(models.Model):
    name = models.CharField(max_length=45)

class Profile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField(max_length=100)
    height = models.SmallIntegerField()
    graduation_year = models.DateField()
    photo = models.CharField(max_length=100)
    institution = models.ForeignKey(Institution)
    is_banned = models.BooleanField(default=False)