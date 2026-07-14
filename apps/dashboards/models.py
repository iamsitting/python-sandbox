from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Dashboard(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    teams = models.ManyToManyField(Team, related_name='dashboards', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name