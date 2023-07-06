/*변수 선언*/

var id = document.querySelector('#id');
var pw1 = document.querySelector('#pswd1');
var pwMsg = document.querySelector('#alertTxt');
var pwImg1 = document.querySelector('#pswd1_img1');
var pw2 = document.querySelector('#pswd2');
var pwImg2 = document.querySelector('#pswd2_img1');
var pwMsgArea = document.querySelector('.int_pass');
var userName = document.querySelector('#name');
var email = document.querySelector('#email');
var mobile = document.querySelector('#phone');
var error = document.querySelectorAll('.error_next_box');

var idPattern = /[a-zA-Z0-9_-]{5,2  0}/;
var pwPattern = /[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]{8,16}/;
var namePattern = /[a-zA-Z가-힣]/;
var emailPattern = /[a-z0-9]{2,}@[a-z0-9-]{2,}\.[a-z0-9]{2,}/;
var isPhoneNum = /^010[0-9]{8}$/;

id.addEventListener("change", checkId);
pw1.addEventListener("change", checkPw);
pw2.addEventListener("change", comparePw);
userName.addEventListener("change", checkName);
email.addEventListener("change", isEmailCorrect);
mobile.addEventListener("change", checkPhoneNum);

/*콜백 함수*/


function checkId() {
    var idPattern = /[a-zA-Z0-9_-]{5,20}/;
    if(id.value === "") {
        error[0].innerHTML = "필수 정보입니다.";
        error[0].style.display = "block";
    } else if(!idPattern.test(id.value)) {
        error[0].innerHTML = "5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다.";
        error[0].style.display = "block";
    } else {
        error[0].innerHTML = "멋진 아이디네요!";
        error[0].style.color = "#08A600";
        error[0].style.display = "block";
    }
}

function checkPw() {
    var pwPattern = /[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]{8,16}/;
    if(pw1.value === "") {
        error[1].innerHTML = "필수 정보입니다.";
        pwMsg.style.display = "block";
        pwMsgArea.style.paddingRight = "40px";

        error[1].style.display = "block";
    } else if(!pwPattern.test(pw1.value)) {
        error[1].innerHTML = "8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요.";
        pwMsg.innerHTML = "사용불가";
        pwMsgArea.style.paddingRight = "93px";
        error[1].style.display = "block";
        pwMsg.style.color = "red";
        pwMsg.style.display = "block";
    } else {
        error[1].style.display = "none";
        pwMsg.innerHTML = "안전";
        pwMsgArea.style.paddingRight = "93px";
        pwMsg.style.color = "#03c75a";
        pwMsg.style.display = "block";
    }
}

function comparePw() {
    if(pw2.value === pw1.value) {
        error[2].style.display = "none";
    } else if(pw2.value !== pw1.value) {
        error[2].innerHTML = "비밀번호가 일치하지 않습니다.";
        error[2].style.display = "block";
    } 

    if(pw2.value === "") {
        error[2].innerHTML = "필수 정보입니다.";
        error[2].style.display = "block";
    }
}

function checkName() {
    var namePattern = /[a-zA-Z가-힣]/;
    if(userName.value === "") {
        error[3].innerHTML = "필수 정보입니다.";
        error[3].style.display = "block";
    } else if(!namePattern.test(userName.value) || userName.value.indexOf(" ") > -1) {
        error[3].innerHTML = "한글과 영문 대 소문자를 사용하세요. (특수기호, 공백 사용 불가)";
        error[3].style.display = "block";
    } else {
        error[3].style.display = "none";
    }
}

function isEmailCorrect() {
    var emailPattern = /[a-z0-9]{2,}@[a-z0-9-]{2,}\.[a-z0-9]{2,}/;

    if(email.value === ""){ 
        error[4].style.display = "none"; 
    } else if(!emailPattern.test(email.value)) {
        error[4].innerHTML = "올바른 이메일 형식이 아닙니다.";
        error[4].style.display = "block";
    } else {
        error[4].style.display = "none"; 
    }

}

function checkPhoneNum() {
    var isPhoneNum = /^010\d{8}$/;  // 전화번호 패턴: '010' 다음에 8자리 숫자

    if(mobile.value === "") {
        error[5].innerHTML = "필수 정보입니다.";
        error[5].style.display = "block";
    } else if(!isPhoneNum.test(mobile.value)) {
        error[5].innerHTML = "올바른 전화번호 형식이 아닙니다.";
        error[5].style.display = "block";
    } else {
        error[5].style.display = "none";
    } 
}


document.querySelector('form').addEventListener("submit", function(event) {
    event.preventDefault();
    var id = document.querySelector("#id").value;
    var pswd1 = document.querySelector("#pswd1").value;
    var pswd2 = document.querySelector("#pswd2").value;
    var name = document.querySelector("#name").value;
    var email = document.querySelector("#email").value;
    var mobile = document.querySelector("#phone").value;


    var idPattern = /^[a-zA-Z0-9]{5,}$/;  // ID 패턴: 영어 알파벳과 숫자로 구성된 5자리 이상
    var phonePattern = /^010\d{8}$/;  // 전화번호 패턴: '010' 다음에 8자리 숫자
    var emailPattern = /[a-z0-9]{2,}@[a-z0-9-]{2,}\.[a-z0-9]{2,}/;  // 이메일 패턴
    var pwPattern = /^(?=.*[a-zA-Z])(?=.*\d).{8,}$/;
    var namePattern = /^[a-zA-Z가-힣]+$/; 

    if (id === "" || pswd1 === "" || pswd2 === "" || name === "" || email === "" || mobile === "") {
        alert("필수 정보를 모두 입력해주세요.");
        event.preventDefault(); // 폼 제출을 막습니다.
    }

    else if (!idPattern.test(id)) {  // ID 패턴 검사
        alert("ID는 영어 알파벳과 숫자로 구성된 5자리 이상이어야 합니다.");
        event.preventDefault(); // 폼 제출을 막습니다.
    }
    else if (!phonePattern.test(mobile)) {  // 전화번호 패턴 검사
        alert("올바른 전화번호 형식이 아닙니다.");
        event.preventDefault(); // 폼 제출을 막습니다.
    }

    else if (!emailPattern.test(email)) {  // 이메일 패턴 검사
        alert("올바른 이메일 형식이 아닙니다.");
        event.preventDefault(); // 폼 제출을 막습니다.
    }

    else if (!pwPattern.test(pswd1)) {  // 비밀번호 패턴 검사
        alert("비밀번호는 영어와 숫자를 포함한 8자리 이상의 문자여야 합니다.");
        event.preventDefault(); // 폼 제출을 막습니다.
    }

    else if (!namePattern.test(name)) {  // 이름 패턴 검사
        alert("이름은 한글과 영문 대 소문자를 사용하세요.");
        event.preventDefault(); // 폼 제출을 막습니다.
    }

    else if (pswd1 !== pswd2) {
        alert("비밀번호를 확인해주세요.");
        event.preventDefault(); // 폼 제출을 막습니다.
    }
    else {
        alert("가입이 완료되었습니다.");
        document.querySelector('form').submit();
    }
});
