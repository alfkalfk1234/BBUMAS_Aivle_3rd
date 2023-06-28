from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'video'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.video_upload, name='video_upload'),
    path("video_db_save/", views.video_db_save, name="video_db_save"),
    path('video/delete/<int:video_id>/', views.delete_video, name='video_delete'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
