const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileReset = document.getElementById('fileReset');
const fileUpload = document.getElementById('fileUpload');

dropZone.addEventListener('dragenter', function(event) {
    event.preventDefault();
    dropZone.classList.add('highlight');
});

dropZone.addEventListener('dragover', function(event) {
    event.preventDefault();
});

dropZone.addEventListener('dragleave', function(event) {
    event.preventDefault();
    dropZone.classList.remove('highlight');
});

dropZone.addEventListener('drop', function(event) {
    event.preventDefault();
    dropZone.classList.remove('highlight');

    handleFileUpload(event.dataTransfer.files[0]);
});

fileInput.addEventListener('change', function(event) {
    handleFileUpload(event.target.files[0]);
});

fileReset.addEventListener('click', function() {
    fileInput.value = ''; // 파일 선택 초기화
    filename.textContent = '';
    filesize.textContent = '';
});

function getFileType(fileName) {
    const extension = fileName.split('.').pop();
    return extension.toLowerCase();
}

function handleFileUpload(file) {
    const fileName = file.name;
    const fileSize = formatFileSize(file.size);
    var src = getFileType(fileName);

    if (src.toLowerCase() == "zip") {
    
        filename.textContent = fileName;
        filesize.textContent = fileSize;

        // 동영상 파일 업로드 처리
        console.log('압축 파일 업로드:', file);

    // avi 파일만 업로드
    } else if (src.toLowerCase() == "avi" ) {
        filename.textContent = fileName;
        filesize.textContent = fileSize;
        // 동영상 파일 업로드 처리
        console.log('영상 파일 업로드:', file);
    } else {
        console.log('유효한 동영상 파일이 아닙니다.');
        alert("블랙박스 영상 파일을 첨부하세요.");
    }
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


// JavaScript to show and hide loader

document.getElementById('fileUpload').addEventListener('click', function() {
    // Show the loading spinner
    document.getElementById('loading').style.display = 'block';
    document.getElementById('loading_msg').style.display = 'block';
    // Hide the dropzone
    document.getElementById('dropZonetext').style.display = 'none';
    });

window.onload = function() {
    // Hide the loading spinner
    document.getElementById('loading').style.display = 'none';
    document.getElementById('loading_msg').style.display = 'none';
    // Show the dropzone
    document.getElementById('dropZonetext').style.display = 'block';
};