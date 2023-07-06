function resetImgForm() {
    const imgForm = document.getElementById("img_form");

    // Clear the filename and filesize elements
    document.getElementById("filename").textContent = "";
    document.getElementById("filesize").textContent = "";

    // Clear the image preview element
    const preview = document.getElementById("preview");
    preview.src = "";
    preview.style.display = "none";

    // Remove image file data
    let fileInput = document.querySelector('#post_image');
    fileInput.value = '';

    document.getElementById("latitude").value = "";
    document.getElementById("longitude").value = "";
  }

// 폼 제출 이벤트
document.querySelector('form').addEventListener('submit', function(e) {
var agreeUseMyInfo = document.querySelector('input[name="agreeUseMyInfo"]:checked').value;
if (agreeUseMyInfo === 'N') {
    alert('개인정보 수집에 동의해주세요'); // 사용자에게 알림
    e.preventDefault(); // 폼 제출 중단
}
});


var geocoder = new kakao.maps.services.Geocoder();


// 지도를 표시할 div와  지도 옵션으로  지도를 생성합니다

function showPopup() {
    // 팝업창을 띄우는 코드 작성
    alert("개인정보 수집에 동의해야 등록할 수 있습니다.");
}

function register() {
    var agreeValue = document.querySelector('input[name="agreeUseMyInfo"]:checked').value;
    if (agreeValue === 'N') {
    showPopup();
    } else {
    // 등록 처리를 진행하는 코드 작성
    // ...
    // 등록 완료 메시지 출력 등
    }
}

function DropFile(dropAreaId, fileListId) {
    let dropArea = document.getElementById(dropAreaId);
    let fileList = document.getElementById(fileListId);

    function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
    }

    function highlight(e) {
    preventDefaults(e);
    dropArea.classList.add("highlight");
    }

    function unhighlight(e) {
    preventDefaults(e);
    dropArea.classList.remove("highlight");
    }

    function handleDrop(e) {
    unhighlight(e);
    let dt = e.dataTransfer;
    let files = dt.files;

    handleFiles(files);

    const fileList = document.getElementById(fileListId);
    if (fileList) {
        fileList.scrollTo({ top: fileList.scrollHeight });
    }
    }

    function handleFiles(files) {
    files = [...files];
    // files.forEach(uploadFile);
    files.forEach(previewFile);
    }

    function previewFile(file) {
    console.log(file);
    renderFile(file);
    }

    function renderFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function () {
        let img = dropArea.getElementsByClassName("preview")[0];
        img.src = reader.result;
        img.style.display = "block";
        handleFileUpload(file);
    };
    }

    dropArea.addEventListener("dragenter", highlight, false);
    dropArea.addEventListener("dragover", highlight, false);
    dropArea.addEventListener("dragleave", unhighlight, false);
    dropArea.addEventListener("drop", handleDrop, false);

    return {
    handleFiles
    };
}

const dropFile = new DropFile("drop-file", "files");


const dropfile = document.getElementById('drop-file');
const chooseFile = document.getElementById('chooseFile');
const selectFile = document.getElementById('selectFile');
const fileReset = document.getElementById('fileReset');
const preview = document.getElementById('preview');

dropfile.addEventListener('drop', function(event) {
    event.stopPropagation();
    event.preventDefault();

    const fileInput = document.getElementById("post_image"); // Change this line
    const file = event.dataTransfer.files[0];
    fileInput.files = event.dataTransfer.files;
    handleFileUpload(event.dataTransfer.files[0]);
});
    
chooseFile.addEventListener('change', function(event) {
    handleFileUpload(event.target.files[0]);
    });

fileReset.addEventListener('click', function() {
    chooseFile.value = ''; // 파일 선택 초기화
    dropfile.value='';
    preview.src = '';
    preview.style.display = 'none';
    fileReset.style.display = 'none';

    // 테이블 초기화
    filename.textContent = '';
    filesize.textContent = '';
    
    selectFile.textContent = '파일 이름: (선택된 파일 없음)'; // 선택한 파일 초기화

    console.log('이미지 파일 업로드:', file);
    });
    let warningDisplayed = false;

    function handleFileUpload(file) {
    let warningDisplayed = false;
    if (file) {
        const fileName = file.name;
        const fileSize = formatFileSize(file.size);

        // 테이블 정보
        filename.textContent = fileName;
        filesize.textContent = fileSize;

        var reader = new FileReader();
        reader.onload = function(e) {
            var imageData = e.target.result;
            var exifData = EXIF.readFromBinaryFile(imageData);

            if (exifData && exifData.GPSLatitude && exifData.GPSLongitude) {
                var latitude = calculateCoordinate(exifData.GPSLatitude);
                var longitude = calculateCoordinate(exifData.GPSLongitude);

                var gpsInfo = latitude + ", " + longitude;


                console.log("사진의 GPS 정보:", gpsInfo);

                document.getElementById('latitude').value = latitude;
                document.getElementById('longitude').value = longitude;
                var position = new kakao.maps.LatLng(latitude, longitude);
                getAddress_post(position);
                // 여기서 주소를 가져옵니다.

            } else {
                if (!warningDisplayed) {
                    alert("GPS 정보가 포함된 이미지를 업로드 해주세요.");
                    warningDisplayed = true;
                }
            }
        };

        reader.readAsArrayBuffer(file);
    }
    }

            
    function getAddress_post(position) {
    geocoder.coord2RegionCode(position.getLng(), position.getLat(), function(result, status) {
        if (status === kakao.maps.services.Status.OK) {
            for (var i = 0; i < result.length; i++) {
                if (result[i].region_type === 'H') { // 행정동의 region_type은 'H'입니다.
                    var address = result[i].region_2depth_name;
                    document.getElementById('address').value = address;
                }
            }
        }
    });
    }



function formatFileSize(size) {
    if (size === 0) {
    return '0 Bytes';
    }
    const units = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const k = 1024;
    const i = Math.floor(Math.log(size) / Math.log(k));
    return parseFloat((size / Math.pow(k, i)).toFixed(2)) + ' ' + units[i];
}


function calculateCoordinate(coordinates) {
    var degree = coordinates[0];
    var minute = coordinates[1];
    var second = coordinates[2];
    var coordinate = ((((degree * 60) + minute) * 60) + second) / 60 / 60;
    return parseFloat(coordinate);
}

// 개인정보 수집 동의 내용보기 버튼
function toggleContent() {
    var singoPerson = document.getElementById("singoPerson");
    var moreBtn = document.querySelector(".moreBtn");
    var moreDoc = document.querySelector('.moreDoc');
    var angleIcon = document.querySelector('.moreBtn i');

    if (singoPerson.style.display === "none") {
    // 숨겨진 상태일 때 보이도록 변경
    singoPerson.style.display = "block";
    moreBtn.classList.add("on");
    moreBtn.innerHTML = '내용닫기  <i class="fa fa-angle-up" aria-hidden="true"></i>';
    } else {
    // 보여지는 상태일 때 숨기도록 변경
    singoPerson.style.display = "none";
    moreBtn.classList.remove("on");
    moreBtn.innerHTML = '내용보기  <i class="fa fa-angle-down" aria-hidden="true"></i>';
    }
}

document.querySelector('.moreBtn').addEventListener('click', toggleContent);