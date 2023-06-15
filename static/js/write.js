// 게시물 배열
const posts = [];

// 게시물을 동적으로 생성하여 게시판에 추가하는 함수
function renderPosts() {
  const board = document.getElementById("board");
  board.innerHTML = ""; // 기존 게시물 삭제

  for (let i = 0; i < posts.length; i++) {
    const post = posts[i];

    // 테이블 행 생성
    const row = document.createElement("tr");

    // 작성일 열 생성
    const dateCell = document.createElement("td");
    dateCell.textContent = post.date;
    dateCell.style.textAlign = "center"; // 가운데 정렬 스타일 추가
    row.appendChild(dateCell);

    // 제목 열 생성
    const titleCell = document.createElement("td");
    titleCell.textContent = post.title;
    titleCell.style.textAlign = "center"; // 가운데 정렬 스타일 추가
    row.appendChild(titleCell);

    // 작성자 열 생성
    const authorCell = document.createElement("td");
    authorCell.textContent = post.author;
    authorCell.style.textAlign = "center"; // 가운데 정렬 스타일 추가
    row.appendChild(authorCell);

    // 테이블에 행 추가
    board.appendChild(row);
  }
}

// 작성 완료 버튼 클릭 이벤트 리스너 등록
const submitBtn = document.getElementById("submitBtn");
submitBtn.addEventListener("click", function() {
  const titleInput = document.getElementById("titleInput");
  const authorInput = document.getElementById("authorInput");
  
  const title = titleInput.value;
  const author = authorInput.value;
  
  if (title && author) {
    const currentDate = new Date().toISOString().split("T")[0]; // 현재 날짜
    const newPost = { date: currentDate, title: title, author: author };
    posts.push(newPost); // 새로운 게시물을 배열에 추가합니다.
    renderPosts(); // 게시판을 업데이트합니다.
  
    // 작성 모달 창 닫기
    closeModal();
  } else {
    alert("제목과 작성자를 입력해주세요.");
  }
});

// 작성하기 버튼 클릭 이벤트 리스너 등록
const writeBtn = document.getElementById("writeBtn");
writeBtn.addEventListener("click", function() {
  // 작성 모달 창 열기
  openModal();
});

// 작성 모달 창 열기 함수
function openModal() {
  const writeModal = document.getElementById("writeModal");
  writeModal.style.display = "block";
}

// 작성 모달 창 닫기 함수
function closeModal() {
  const writeModal = document.getElementById("writeModal");
  writeModal.style.display = "none";
}

// 초기 실행
document.addEventListener("DOMContentLoaded", function() {
  renderPosts();
});











