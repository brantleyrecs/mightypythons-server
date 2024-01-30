from django.db import models
from .destination import Destination
from .activity import Activity

class DestAct(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='dest_activities')