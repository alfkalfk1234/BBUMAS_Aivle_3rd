from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Photo
from .forms import PostForm
from .utils import create_post
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO

from django.http import JsonResponse
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post/post.html', {'posts': posts})

# def posting(request):
#     return render(request, 'post/service-details.html')

import os, shutil, re
from django.core.files import File 
from django.conf import settings 

def posting(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        
        if form.is_valid():
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            region = request.POST.get('address')
            post = form.save(commit=False)
            post.post_latitude = latitude
            post.post_longitude = longitude
            post.post_region = region
            post.author = request.user  # set author as the current user
            post.save()
            
            img = post.post_image.url
            analyze_photo(img)
            file_name = re.search(r'images/(.+)', img).group(1)
            yolo_img_path = f'video/media/predict/{file_name}'
            rel_path = os.path.relpath(yolo_img_path, settings.MEDIA_ROOT) 
            post.detected_image.save(rel_path, File(open(yolo_img_path, 'rb')), save=True)
            
            shutil.rmtree('video/media/predict')
            return redirect('post:post')
    else:
        form = PostForm()
    return render(request, 'post/service-details.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'post/post_detail.html', {'post': post})


def faq(request):
    return render(request, 'post/faq.html')

@csrf_exempt
def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        post.delete()
        return JsonResponse({'success': True})

def analyze_photo(photo_path):
    # YOLOv8 analysis code
    yolov8_model_path = 'video/tool/custom_yolov8m_0628_2.pt'
    model = YOLO(yolov8_model_path)
    model.predict(
        source = photo_path,
        conf = 0.65,
        iou = 0.15,
        save = True,
        project = 'video/media',
        classes = [0, 1, 3, 4, 5, 7, 8], # road-marking + lane
        # names: {0: 'Pothole', 1: 'bollard_abnormal', 2: 'bollard_normal', 3: 'crosswalk', 4: 'road-marking', 5: 'road_separator_abnormal', 
        # 6: 'road_separator_normal', 7: 'speedbump', 8: 'tubular-marker-abnormal', 9: 'tubular-marker-normal', 10: 'loading-box'}
    )