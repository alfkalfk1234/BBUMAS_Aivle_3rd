from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='')

class Detection(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()
    detected_object = models.IntegerField()
    image_path = models.CharField(max_length=200)
    frame = models.IntegerField()

