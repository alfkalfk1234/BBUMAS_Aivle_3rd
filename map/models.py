from django.db import models

class Location_test(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    time = models.DateTimeField()
    detected_object = models.CharField(max_length=200) # 검출물
