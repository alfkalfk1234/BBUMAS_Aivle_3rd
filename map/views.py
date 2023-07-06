from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import Location,Location_test
from post.models import Post
from video.models import Detected
from join.models import CustomUser

def index(request):
    return render(request, 'map/map.html')

# get_locations 창으로 DB 내부 정보 확인용
def get_locations(request):
    locations_post = Post.objects.all()
    location_posts = [[loc.post_latitude, loc.post_longitude, loc.report_type,loc.detected_image.url,loc.pk,loc.post_region] for loc in locations_post]    # location_list = serializers.serialize('json', locations)  # QuerySet을 JSON으로 변환
    return JsonResponse(location_posts, safe=False)  # JSON 응답 반환

# DB에서 정보 가져와서 리스트로 변환 후 html로 정보 전송
def map_view(request):
    locations_post = Post.objects.all()
    locations_video = Detected.objects.all()

    # 로그인된 사용자의 경우
    if request.user.is_authenticated and request.user.region != ' ':
        # 현재 로그인한 사용자의 region을 가져옵니다.
        current_user_region = request.user.region

        # 현재 사용자의 region에 해당하는 post만을 가져옵니다.
        locations_post = locations_post.filter(post_region=current_user_region)
        locations_video = locations_video.filter(video_region=current_user_region)


        user_region = [[current_user_region]]
    # 로그인되지 않은 사용자의 경우 혹은 region이 기본값인 경우
    else:
        user_region = []

    location_posts = [[loc.post_latitude, loc.post_longitude, loc.report_type,loc.detected_image.url,loc.pk,loc.post_region] for loc in locations_post]
    location_videos = [[loc.latitude, loc.longitude, loc.detected_object,loc.image_path,loc.pk,loc.video_region] for loc in locations_video]

    context = {
        'location_posts': location_posts,
        'location_videos': location_videos,
        'user_region' : user_region,
    }

    return render(request, 'map/map.html', context)




