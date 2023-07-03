from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(max_length=100, default=1)

class Detection(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, default=1)
    latitude = models.FloatField()
    longitude = models.FloatField()
    detected_object = models.CharField(max_length=200, null=True)
    detected_time = models.CharField(max_length=200, null=True)
    detected_where = models.CharField(max_length=200, null=True)
    image_path = models.URLField(max_length=200, null=True)
    def __str__(self):
        return f"Detection {self.pk}"

class Damage(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    department = models.CharField(max_length=100)
    imaga_name = models.CharField(max_length=100)

    def save_to_mysql(self):
        self.save()
        
class Detected(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    detected_object = models.CharField(max_length=200, null=True)
    detected_time = models.CharField(max_length=200, null=True)
    detected_where = models.CharField(max_length=200, null=True)
    image_path = models.CharField(max_length=200, null=True, blank=True)
    video_region = models.CharField(max_length=150, blank=False, null=False, default=' ')

    def __str__(self):
        return f"Detected {self.pk}"