from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import Location,Location_test
from post.models import Post
from video.models import Detected

def index(request):
    return render(request, 'map/map.html')

# get_locations 창으로 DB 내부 정보 확인용
def get_locations(request):
    locations_video = Detected.objects.all()
    location_videos = [[loc.latitude, loc.longitude, loc.detected_object,loc.image_path,loc.pk] for loc in locations_video]
    # location_list = serializers.serialize('json', locations)  # QuerySet을 JSON으로 변환
    return JsonResponse(location_videos, safe=False)  # JSON 응답 반환

# DB에서 정보 가져와서 리스트로 변환 후 html로 정보 전송
def map_view(request):
    locations_post = Post.objects.all()
    locations_video = Detected.objects.all()
    location_posts = [[loc.post_latitude, loc.post_longitude, loc.report_type,loc.post_image.url,loc.pk] for loc in locations_post]
    location_videos = [[loc.latitude, loc.longitude, loc.detected_object,loc.image_path,loc.pk] for loc in locations_video]
    context = {
        'location_posts': location_posts,
        'location_videos': location_videos
    }

    return render(request, 'map/map.html', context)

