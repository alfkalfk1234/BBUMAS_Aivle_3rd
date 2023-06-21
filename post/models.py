from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Photo(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()
    detected_object = models.CharField(max_length=100)
    photo_path = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.detected_object

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
