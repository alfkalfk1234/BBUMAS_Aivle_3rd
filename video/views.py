from django.shortcuts import render
from django.http import JsonResponse
from .models import Detected
from .models import Video,Detected
from storages.backends.s3boto3 import S3Boto3Storage
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO
import urllib.parse
import os
import subprocess
import time
import struct
import pandas as pd
import cv2
import shutil
import pytz
from datetime import datetime
import json

def index(request):
    return render(request, 'video/video.html')

def analyze_video(video_path):
    # YOLOv8 analysis code
    yolov8_model_path = 'video/tool/custom_yolov8m_0628_2.pt'
    model = YOLO(yolov8_model_path)
    model.predict(
        source = video_path,
        conf = 0.85,
        iou = 0.15,
        save = True,
        save_txt = True,
        project = 'video/media',
        classes = [0, 1, 3, 4, 5, 7, 8],
        # names: {0: 'Pothole', 1: 'bollard_abnormal', 2: 'bollard_normal', 3: 'crosswalk', 4: 'road-marking', 5: 'road_separator_abnormal', 6: 'road_separator_normal', 7: 'speedbump', 8: 'tubular-marker-abnormal', 9: 'tubular-marker-normal'}
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
        time_converted_value_utc = datetime.utcfromtimestamp(time_converted_value)

        kst = pytz.timezone('Asia/Seoul')
        time_converted_value_kst = kst.localize(time_converted_value_utc)
        
        formattime = time_converted_value_kst.strftime('%Y. %m. %d.  %H시 %M분 %S초')
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
        # media 초기화
        try:
            shutil.rmtree('video/media')
        except:
            pass
        os.mkdir('video/media')
        
        video_file = request.FILES['video_file']
        title = video_file.name

        video = Video(title=title, video_file=video_file)
        # video.save()

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
        # 파손 내용이 없을 시에 알람 및 비디오 페이지로 이동
        if info.empty:
            message = '파손 내용이 없습니다!'
            return render(request, 'video/video.html', {'message': message})
        
        info['second'] = info['frame'] // 30

        # Dataframe 결합(위치정보 + 손상정보)
        all = pd.merge(left = latlng , right = info, how = "inner", on = "second")
        
        # 위, 경도 중복시 중복 행 제거 - 1초에 한 프레임만 선택 (임시.. 추후 개선)
        all = all.drop_duplicates(subset=['latitude', 'longitude'], keep='first')
        
        # 클래스 이름과 클래스 번호 분리
        all['class_num'] = all['class_name'].copy()
        all.loc[all["class_name"] == '0', "class_name"] = '포트홀'
        all.loc[all["class_name"] == '1', "class_name"] = '볼라드 손상'
        all.loc[all["class_name"] == '2', "class_name"] = '볼라드 정상'
        all.loc[all["class_name"] == '3', "class_name"] = '횡단보도 손상'
        all.loc[all["class_name"] == '4', "class_name"] = '도로 표지 손상'
        all.loc[all["class_name"] == '5', "class_name"] = '도로 분리대 손상'
        all.loc[all["class_name"] == '6', "class_name"] = '도로 분리대 정상'
        all.loc[all["class_name"] == '7', "class_name"] = '방지턱 손상'
        all.loc[all["class_name"] == '8', "class_name"] = '시선 유도봉 손상'
        all.loc[all["class_name"] == '9', "class_name"] = '시선 유도봉 정상'
        
        # names: {0: 'Pothole', 1: 'bollard_abnormal', 2: 'bollard_normal', 3: 'crosswalk', 4: 'road-marking', 5: 'road_separator_abnormal', 
        # 6: 'road_separator_normal', 7: 'speedbump', 8: 'tubular-marker-abnormal', 9: 'tubular-marker-normal'}
        all['where'] = '도로 교통과'
        all['id'] = range(1, len(all) + 1)
        print(all)
        results = all.to_dict(orient='records')
        json_data = json.dumps(results, ensure_ascii=False)
        context = {'results' : json_data}
        return render(request, 'video/video_result.html', context)
    else:
        return render(request, 'video/video.html')

def video_db_save(request):
    if request.method == "POST":
        data = urllib.parse.unquote(request.body.decode('utf-8'))
        if data.startswith('data='):
            data = data[5:] # 'data=' 제거
            print(data)
            try:
                data = json.loads(data)
                for item in data:
                    detection = Detected.objects.create(
                        detected_time = item["time"],
                        detected_object = item["class_name"],
                        detected_where = item["where"],
                        latitude = item.get("latitude", ""),
                        longitude = item.get("longitude", ""),
                        image_path= item["file_path"],
                    )
                    storage = S3Boto3Storage()
                    fromfilepath = 'video/media/images/' + item["file_path"]
                    tofilepath = 'video/' + item["file_path"]
                    storage.save(tofilepath, open(fromfilepath, 'rb'))
                    # detection.image_path = filepath
                    detection.save()
                    
                print("MySQL DataBase Upload success")
                return JsonResponse({"success": True})
            except json.JSONDecodeError:
                print("error: Invalid JSON data")
                return JsonResponse({"success": False, "error": "Invalid JSON data"})
        else:
            print("error: Invalid data format")
            return JsonResponse({"success": False, "error": "Invalid data format"})
    else:
        print("error: Invalid request method")
        return JsonResponse({"success": False, "error": "Invalid request method"})

@csrf_exempt
def delete_video(request, video_id):
    if request.method == 'POST':
        post = Detected.objects.get(pk=video_id)
        post.delete()
        return JsonResponse({'success': True})