// Reference the toggle button & dropdown menu for Add Layer page
const toggleButton = document.getElementById('group-select');
const dropdownMenu =document.getElementById('dropdown-menu');

// Track if the dropdown is open
let isDropdownOpen = false;

// Prevent the dropdown from closing when clicking anywhere inside
dropdownMenu.addEventListener('click', (event) => {
    event.stopPropagation(); // Stops the click event from propagating
});