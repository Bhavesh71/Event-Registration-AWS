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