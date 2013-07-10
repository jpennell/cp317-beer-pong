from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    height = models.SmallIntegerField()
    graduation_year = models.DateField()
    photo = ImageField()
    institution_id = models.ForeignKey(Institution)
    is_banned = models.BooleanField()
    
    
class Institution(models.Model):
    name = models.CharField(max_length=45)