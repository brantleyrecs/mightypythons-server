from django.db import models

class Climate(models.Model):
    name = models.CharField(max_length=50)