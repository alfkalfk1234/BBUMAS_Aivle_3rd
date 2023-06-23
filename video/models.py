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
    is_checked = models.BooleanField(default=False)

class Damage(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    department = models.CharField(max_length=100)
    imaga_name = models.CharField(max_length=100)

    def save_to_mysql(self):
        self.save()