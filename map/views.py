from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import Location,Location_test

def index(request):
    return render(request, 'map/map.html')

# get_locations 창으로 DB 내부 정보 확인용
def get_locations(request):
    locations = Location_test.objects.all()  # 모든 위치 데이터를 가져옵니다
    location_list = serializers.serialize('json', locations)  # QuerySet을 JSON으로 변환
    return JsonResponse(location_list, safe=False)  # JSON 응답 반환

# DB에서 정보 가져와서 리스트로 변환 후 html로 정보 전송
def map_view(request):
    locations = Location_test.objects.all()
    location_list = [[loc.latitude, loc.longitude, loc.detect_type] for loc in locations]
    
    return render(request, 'map/map.html', {'locations': location_list})