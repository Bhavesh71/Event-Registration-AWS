let currentIndex = 0;
const totalImages = 10; // Total number of images/texts
const intervalTime = 3000; // Time in milliseconds for each slide

function showSlide(index) {
    const images = document.querySelectorAll('.cimg');
    const texts = document.querySelectorAll('.ctext');
    const dots = document.querySelectorAll('.dot');

    images.forEach((img, i) => {
        img.style.display = (i === index) ? 'block' : 'none';
    });

    texts.forEach((text, i) => {
        text.style.display = (i === index) ? 'block' : 'none';
    });

    dots.forEach((dot, i) => {
        dot.classList.toggle('on', i === index);
    });
}

function nextSlide() {
    currentIndex = (currentIndex + 1) % totalImages;
    showSlide(currentIndex);
}

// Initial call
showSlide(currentIndex);
setInterval(nextSlide, intervalTime);


document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.querySelector('.dropdown');
    const toggleButton = document.querySelector('.dropdown-toggle');

    // Toggle dropdown visibility on button click
    toggleButton.addEventListener('click', function () {
        dropdown.classList.toggle('show');
    });

    // Close dropdown if clicked outside
    window.addEventListener('click', function (event) {
        if (!dropdown.contains(event.target)) {
            dropdown.classList.remove('show');
        }
    });
});