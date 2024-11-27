// Reference toggle buttons & dropdown menus in Add Layer page
const departmentToggleButton = document.getElementById('department-select');
const groupToggleButton = document.getElementById('group-select');

const departmentDropdownMenu = document.getElementById('department-dropdown');
const groupDropdownMenu = document.getElementById('group-dropdown');


// Prevent dropdown from closing when clicking anywhere inside 'Department' & 'Group'
departmentDropdownMenu.addEventListener('click', (event) => {
    event.stopPropagation(); // Stops the click event from propagating
});

groupDropdownMenu.addEventListener('click', (event) => {
    event.stopPropagation(); // Stops the click event from propagating
});