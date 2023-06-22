from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'video'
urlpatterns = [
    path('', views.index, name='video'),
    path('upload/', views.video_upload, name='video_upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
