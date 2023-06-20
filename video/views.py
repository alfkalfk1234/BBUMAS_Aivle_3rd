from django.shortcuts import render, redirect
from .models import Video
from ultralytics import YOLO
import os
import subprocess
import time
import struct
import pandas as pd
from datetime import datetime, timedelta

def index(request):
    return render(request, 'video/video.html')

def video_result(request):
    return render(request, 'video/video_result.html')

def analyze_video(video_path):
    # YOLOv8 analysis code
    yolov8_model_path = 'video/tool/yolov8n.pt'
    model = YOLO(yolov8_model_path)
    model.predict(
        source = video_path,
        conf = 0.5,
        iou = 0.3,
        save = True,
        save_txt = True,
        project = 'video/media',
        # classes = [0, 2, 3, 4, 5, 7, 8, 9, 10],
    )
    result = "YOLOv8 analysis result"
    return result

def get_latlng(path,video_path):
    idx = []
    geo_bins = []
    geo = []
    
    name,ext = os.path.splitext(video_path)
    # createDir(f'{path}/bin')
    # os.mkdir(f'{path}/bin')
    if ext =='.avi' or ext=='.mp4':
        file_name = name

        input_file = f"{path}/{file_name}.avi"
        output_file = f"{path}/bin/{file_name}.bin"

        command = ["video/tool/ffmpeg","-i", input_file,"-map","0:3","-c","copy","-f", "data", output_file]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        print(f'{output_file} 저장')
    else:
        print('등록된 확장자가 아닙니다.')
    time.sleep(2)    
    with open(f"{path}/bin/{file_name}.bin",'rb') as file:
        data = file.read()
        for i in range(0,len(data), 72):
            idx.append({'offset':i,'lat_idx':i+60,'lng_idx':i+64, 'time':i+68})
        for offset in idx:
            lat_idx = offset['lat_idx']
            lng_idx = offset['lng_idx']
            time_idx = offset['time']
            file.seek(lat_idx)
            lat_bin = file.read(4)
            file.seek(lng_idx)
            lng_bin = file.read(4)
            file.seek(time_idx)
            time_bin = file.read(4)
            # 중복 제거
            if (lat_bin, lng_bin, time_bin) not in geo_bins:
                geo_bins.append((lat_bin, lng_bin, time_bin))

    for geo_bin in geo_bins:
        lat_binary_data = geo_bin[0]
        lat_converted_value = struct.unpack('<f', lat_binary_data)[0]

        lng_binary_data = geo_bin[1]
        lng_converted_value = struct.unpack('<f', lng_binary_data)[0]
        
        time_binarydata = geo_bin[2]
        time_converted_value = struct.unpack('<I', time_binarydata)[0]
        time_converted_value = datetime.fromtimestamp(time_converted_value)
        formattime = time_converted_value.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')
        geo.append({'lat':round(lat_converted_value,6),'lng':round(lng_converted_value,6), 'time':formattime})
    
        
    return geo

def extract_latitude_longitude(string):
    # 위도와 경도 값 추출
    latitude = string['lat']
    longitude = string['lng']
    time = string['time']
    lat = convert_to_degrees(latitude)
    lng = convert_to_degrees(longitude)
    return lat, lng, time

def convert_to_degrees(coord):
    # 위도 또는 경도 값에서 필요한 정보 추출
    coord = str(coord)
    digit = coord.split('.')
    if len(digit[0]) > 4:
        length = 3
    else:
        length = 2
    degrees = int(coord[:length])
    minutes = float(coord[length:])
    # 분을 계산
    minutes_decimal = (minutes % 100) / 60.0
    # 도와 분을 합하여 실제 좌표 값 계산
    result = degrees + minutes_decimal

    # 북위(S), 남위(N), 서경(W)와, 동경(E)을 고려해 부호 조정
    if coord[-1] in ['S', 'W']:
        result *= -1

    return round(result,7)

def extract_latitude_longitude(string):
    # 위도와 경도 값 추출
    latitude = string['lat']
    longitude = string['lng']
    time = string['time']
    lat = convert_to_degrees(latitude)
    lng = convert_to_degrees(longitude)
    return lat, lng, time

def convert_to_degrees(coord):
    # 위도 또는 경도 값에서 필요한 정보 추출
    coord = str(coord)
    digit = coord.split('.')
    if len(digit[0]) > 4:
        length = 3
    else:
        length = 2
    degrees = int(coord[:length])
    minutes = float(coord[length:])
    # 분을 계산
    minutes_decimal = (minutes % 100) / 60.0
    # 도와 분을 합하여 실제 좌표 값 계산
    result = degrees + minutes_decimal

    # 북위(S), 남위(N), 서경(W)와, 동경(E)을 고려해 부호 조정
    if coord[-1] in ['S', 'W']:
        result *= -1

    return round(result,7)

# def video_result(request, result):
#     return render(request, 'video/video_result.html', {'result': result})
def video_result(request):
    return render(request, 'video/video_result.html')

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

        path = 'video/media/'
        filename = video.video_file.name
        L = get_latlng(path, filename)
        LL = []
        for latlng in L:
            tmp = extract_latitude_longitude(latlng)
            LL.append(tmp)
        latlng = pd.DataFrame(LL, columns=['latitude', 'longitude', 'time'])
        latlng.to_csv(f'video/media/csv/{video.video_file.name[:-4]}.csv', index=False, encoding='utf-8-sig')

        # yolov8 분석
        result = analyze_video(video_path)

        # return redirect('video:video_result', result=result)
        return redirect('video:video_result')
    else:
        return render(request, 'video/video.html')