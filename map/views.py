from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import Location

def index(request):
    return render(request, 'map/map.html')

def get_locations(request):
    locations = Location.objects.all()  # 모든 위치 데이터를 가져옵니다
    location_list = serializers.serialize('json', locations)  # QuerySet을 JSON으로 변환
    return JsonResponse(location_list, safe=False)  # JSON 응답 반환