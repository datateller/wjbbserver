from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Baby(models.Model):
    name = models.TextField(max_length=40,null=True)
    birthday = models.DateField(null=True)
    sex = models.TextField(max_length=10,null=True)
    weight = models.FloatField(2,null=True)
    height = models.FloatField(2,null=True)
    parent_id = models.IntegerField(10,null=True)