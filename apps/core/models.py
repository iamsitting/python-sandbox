from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Teams model where users can be assigned to multiple teams. Each team has a name

class Team(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='teams')

    def __str__(self):
        return self.name