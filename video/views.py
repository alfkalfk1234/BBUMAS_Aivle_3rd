import os
from django.shortcuts import render, redirect
from .models import Video
from ultralytics import YOLO

def analyze_video(video_path):
    # YOLOv8 analysis code
    yolov8_model_path = 'video/yolov8_model/yolov8n.pt'
    model = YOLO(yolov8_model_path)
    model.predict(
        source = video_path,
        conf = 0.5,
        iou = 0.3,
        save = True,
        save_txt = True,
        # classes = [0, 2, 3, 4, 5, 7, 8, 9, 10],
    )
    result = "YOLOv8 analysis result"
    return result

def index(request):
    return render(request, 'video/video.html')

def videoresult(request):
    return render(request, 'video/videoresult.html')

def video_upload(request):
    if request.method == 'POST' and request.FILES['video_file']:
        video_file = request.FILES['video_file']
        title = video_file.name

        video = Video(title=title, video_file=video_file)
        video.save()

        video_path = os.path.join('video/media', video.video_file.name)
        with open(video_path, 'wb') as file:
            for chunk in video_file.chunks():
                file.write(chunk)

        result = analyze_video(video_path)

        return redirect('video:video_result', result=result)
    else:
        return render(request, 'video/video.html')

def video_result(request, result):
    return render(request, 'video/video_result.html', {'result': result})
