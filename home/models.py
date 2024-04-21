from django.db import models


class Events(models.Model):
    name = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    drivers = models.JSONField()


class Users(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
