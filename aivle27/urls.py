from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def index(request):
    return render(request,'index.html')

urlpatterns = [
    path('', index),
    path("admin/", admin.site.urls),
    path('video/', include('video.urls')),
    path('post/', include('post.urls')),
    path('map/', include('map.urls')),
    path('login/', include('login.urls')),
    path('join/', include('join.urls')),
]
