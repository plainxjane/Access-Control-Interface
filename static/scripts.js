// Reference toggle buttons & dropdown menus in Add Layer page
const toggleButton = document.querySelectorAll('.dropdown-toggle');
const dropdownMenu = document.querySelectorAll('.dropdown-menu');


// Prevent dropdown from closing when clicking anywhere inside dropdown menu
dropdownMenu.forEach((menu) => {
    menu.addEventListener('click', (event) => {
        event.stopPropagation(); // Stops the click event from propagating
    });
});

// Initialize Bootstrap popover function
    document.addEventListener('DOMContentLoaded', function () {
        var popoverElements = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverElements.forEach(function (popoverElement) {
            new bootstrap.Popover(popoverElement, {
                html: true // Enable HTML content
            });
        });
    });
