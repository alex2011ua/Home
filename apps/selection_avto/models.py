from django.db import models


class Avto(models.Model):
    date_message = models.DateTimeField()
    autoId = models.CharField(max_length=40, unique=True)
    raceInt = models.IntegerField(null=True)
    USD = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    markName = models.CharField(max_length=40)
    modelName = models.CharField(max_length=40)
    linkToView = models.CharField(max_length=140)
    foto = models.CharField(max_length=140, null=True)
    bodyId = models.CharField(max_length=40, null=True)
