from django.db import models
from .user import User

class Destination(models.Model):
  name = models.CharField(max_length=50)
  bio = models.CharField(max_length=500)
  image=models.CharField(max_length=50)
  user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=0, related_name='user')
