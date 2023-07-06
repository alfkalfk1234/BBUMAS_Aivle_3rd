from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
class Photo(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()
    detected_object = models.CharField(max_length=100)
    photo_path = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.detected_object

class Post(models.Model):
    REPORT_TYPES = (
        ('none', '신고 유형'),
        ('bollard','볼라드 손상'),
        ('crosswalk', '횡단보도 손상'),
        ('snowbox', '제설함 손상'),
        ('pothole', '포트홀'),
        ('road_barrier_damage', '도로 분리대 손상'),
        ('lane', '도로 표시 손상'),
        ('speed_bump', '방지턱'),
        ('tubular_marker', '시선 유도봉'),
    )
    post_title = models.CharField(max_length=200)
    post_content = models.TextField(null=True, blank=True)
    post_image = models.ImageField(upload_to='images/', null=True, blank=True)
    detected_image = models.ImageField(upload_to='', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    post_latitude = models.FloatField(null=True, blank=True)
    post_longitude = models.FloatField(null=True, blank=True)
    post_region = models.CharField(max_length=150, blank=False, null=False, default=' ')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, default='none')

    def save(self, *args, **kwargs):
        if self.report_type == 'none':
            return  # 'none'일 때 저장하지 않음
        else:
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.post_title
