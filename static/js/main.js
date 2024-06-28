document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var flashMessage = document.getElementById('flash-message');
        if (flashMessage !== null) {
            flashMessage.style.display = 'none';
        }
    }, 3000);
  });