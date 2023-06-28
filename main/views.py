from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from post.models import Post
from video.models import Detected


def index(request):
    locations_post = Post.objects.all()
    locations_video = Detected.objects.all()
    location_posts = [[loc.post_latitude, loc.post_longitude, loc.report_type,loc.post_image.url,loc.pk] for loc in locations_post]
    location_videos = [[loc.latitude, loc.longitude, loc.detected_object,loc.image_path,loc.pk] for loc in locations_video]
    context = {
        'location_posts': location_posts,
        'location_videos': location_videos
    }

    return render(request, 'main/index.html', context)