from django.contrib.auth.models import User
from django.db import models

class UserExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15,blank=True,null=True)