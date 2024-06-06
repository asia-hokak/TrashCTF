document.addEventListener('DOMContentLoaded', function() {
    const delay = 2000; // 2 seconds

    const element = document.getElementById('title');

    setTimeout(function() {
        element.classList.remove('hidden');
        element.classList.add('slideUp');
        
    }, delay);
});