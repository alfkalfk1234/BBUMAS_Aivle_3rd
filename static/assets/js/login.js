window.onload = function() {
    var error_message = document.getElementById('error-message');
    if (error_message) {
      setTimeout(function() {
        error_message.style.display = 'none';
      }, 3000);  // 3초 후에 사라짐
    }
  };