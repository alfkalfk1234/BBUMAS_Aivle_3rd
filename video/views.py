from django.shortcuts import render, redirect
from .forms import DamageForm
from .models import Damage
from .models import Video,Detection
from ultralytics import YOLO
import os
import subprocess
import time
import struct
import pandas as pd
import cv2
import shutil
from datetime import datetime

def index(request):
    return render(request, 'video/video.html')

def video(request):
    if request.method == 'POST':
        form = DamageForm(request.POST)
        if form.is_valid():
            selected_damages = form.cleaned_data.get('damages', [])
            for damage_id in selected_damages:
                damage = Damage.objects.get(id=damage_id)
                # 선택된 파손 정보를 MySQL 데이터베이스에 저장
                damage.save_to_mysql()
            return redirect('video')  # 저장 후 video 페이지로 이동
    else:
        form = DamageForm()

    damages = Damage.objects.all()
    return render(request, 'video.html', {'form': form, 'damages': damages})

# def video_result(request):
#     damages = Damage.objects.all()
#     return render(request, 'video_result.html', {'damages': damages})

def analyze_video(video_path):
    # YOLOv8 analysis code
    yolov8_model_path = 'video/tool/custom_yolov8m_0619.pt'
    model = YOLO(yolov8_model_path)
    model.predict(
        source = video_path,
        conf = 0.5,
        iou = 0.3,
        save = True,
        save_txt = True,
        project = 'video/media',
        classes = [0, 2, 3, 4, 5, 7, 8, 9],
        # names: {0: 'bollard_abnormal', 1: 'bollard_normal', 2: 'crosswalk', 3: 'loading-box', 4: 'pothole', 5: 'road_separator', 6: 'road_separator_normal', 7: 'roadmarking', 8: 'speedbump', 9: 'tubular-marker-abnormal'}
    )

    os.remove(video_path)
    return 0

def get_latlng(path,video_path):
    idx = []
    geo_bins = []
    geo = []
    
    name,ext = os.path.splitext(video_path)
    os.mkdir(f'{path}/bin')
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
        formattime = time_converted_value.strftime('%Y. %m. %d. %H. %M. %S')
        geo.append({'lat':round(lat_converted_value,6),'lng':round(lng_converted_value,6), 'time':formattime})
    
    shutil.rmtree(f'{path}/bin')
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


def save_images(video_file_name):
    # 비디오 파일 열기
    video_path = f'video/media/predict/{video_file_name[:-4]}.mp4'
    # video_path = f'video/media/predict/20230618-12h41m41s_N.mp4'
    video_name = os.path.splitext(os.path.basename(video_path))[0]  # 비디오 파일의 이름 추출
    video_capture = cv2.VideoCapture(video_path)

    # 프레임 번호와 클래스 내용을 담을 딕셔너리
    frame_info = {}

    # 텍스트 파일들이 위치한 폴더 경로
    txt_folder = 'video/media/predict/labels'

    # 폴더 내의 모든 텍스트 파일을 검색하여 프레임 번호와 클래스 내용 추출
    for file_name in os.listdir(txt_folder):
        if file_name.endswith('.txt'):
            txt_file = os.path.join(txt_folder, file_name)
            frame_number = int(file_name.split('_')[-1].split('.')[0]) - 1  # 제목에서 프레임 번호 추출
            with open(txt_file, 'r') as file:
                class_name = file.readline().split()[0]  # 첫 번째 숫자를 클래스 내용으로 추출
                frame_info[frame_number] = class_name

    # 프레임 단위로 영상 캡쳐
    frame_count = 0
    info = []

    os.mkdir('video/media/images')
    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            break

        if frame_count in frame_info:
            class_name = frame_info[frame_count]  # 프레임 번호에 해당하는 클래스 내용 가져오기

            # 특정 프레임에 대한 처리
            # 예: 프레임 저장, 작업 수행 등
            file_name = f'video/media/images/{video_name}_{frame_count+1}_{class_name}.jpg'
            cv2.imwrite(file_name, frame)
            only_file_name = f'{video_name}_{frame_count+1}_{class_name}.jpg'
            info.append({'frame' : frame_count+1, 'class_name' : class_name, 'file_name' : only_file_name})
            del frame_info[frame_count]  # 이미 처리한 프레임은 딕셔너리에서 제거

            if not frame_info:  # 모든 프레임을 처리했으면 종료
                break

        frame_count += 1

    # 비디오 캡처 종료
    video_capture.release()
    cv2.destroyAllWindows()

    os.remove(video_path)
    shutil.rmtree('video/media/predict')
    return info

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

        # 위치 정보 csv 파일로 저장
        path = 'video/media/'
        filename = video.video_file.name
        L = get_latlng(path, filename)
        LL = []
        for latlng in L:
            tmp = extract_latitude_longitude(latlng)
            LL.append(tmp)
        latlng = pd.DataFrame(LL, columns=['latitude', 'longitude', 'time'])
        length = len(LL)
        second = [i for i in range(length)]
        latlng['second'] = second

        # yolov8 분석
        analyze_video(video_path)

        # yolov8 분석 영상을 이미지로
        info = save_images(filename) # frame, class_name, file_name
        info = pd.DataFrame(info)
        info['second'] = info['frame'] // 30

        # Dataframe 결합(위치정보 + 손상정보)
        all = pd.merge(left = latlng , right = info, how = "inner", on = "second")
        all.loc[all["class_name"] == '0', "class_name"] = '볼라드 손상'
        all.loc[all["class_name"] == '1', "class_name"] = '볼라드 정상'
        all.loc[all["class_name"] == '2', "class_name"] = '횡단보도 손상'
        all.loc[all["class_name"] == '3', "class_name"] = '제설함 손상'
        all.loc[all["class_name"] == '4', "class_name"] = '포트홀'
        all.loc[all["class_name"] == '5', "class_name"] = '도로 분리대 손상'
        all.loc[all["class_name"] == '6', "class_name"] = '도로 분리대 정상'
        all.loc[all["class_name"] == '7', "class_name"] = '도로 표지 손상'
        all.loc[all["class_name"] == '8', "class_name"] = '방지턱 손상'
        all.loc[all["class_name"] == '9', "class_name"] = '시선 유도봉 손상'
        all.loc[all["class_name"] == '10', "class_name"] = '시선 유도봉 정상'
        
        all['where'] = '도로 교통과'
        all['id'] = range(1, len(all) + 1)
        print(all)
        results = all.to_dict(orient='records')
        context = {'results' : results}
        return render(request, 'video/video_result.html', context)
    else:
        return render(request, 'video/video.html')
    
    
# def save_detection_data(latitude, longitude, time, detection_info, image_path, frame):
#     detection = Detection()
#     detection.latitude = latitude
#     detection.longitude = longitude
#     detection.time = time
#     detection.detection_info = detection_info
#     detection.image_path = image_path
#     detection.frame = frame
#     detection.save()