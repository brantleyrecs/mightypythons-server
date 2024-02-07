from django.db import models
from .user import User
from .climate import Climate

class Destination(models.Model):
  name = models.CharField(max_length=50)
  bio = models.CharField(max_length=500)
  image=models.CharField(max_length=50)
  climate=models.ForeignKey(Climate, on_delete=models.CASCADE, related_name='climate')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
  favorite = models.BooleanField(default=False)
