from django.urls import path
from . import views

app_name = 'video'
urlpatterns = [
    path('', views.index, name='video'),
    path('upload/', views.video_upload, name='video_upload'),
    path('result/<str:result>/', views.video_result, name='video_result'),
]
