// Reference toggle buttons & dropdown menus in Add Layer/Add User/Update User pages
const toggleButton = document.querySelectorAll('.dropdown-toggle');
const dropdownMenu = document.querySelectorAll('.dropdown-menu');


// Prevent dropdown from closing when clicking anywhere inside dropdown menu
dropdownMenu.forEach((menu) => {
    menu.addEventListener('click', (event) => {
        event.stopPropagation(); // Stops the click event from propagating
    });
});

// Initialize Bootstrap Popover function
document.addEventListener('DOMContentLoaded', function () {
    var popoverElements = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverElements.forEach(function (popoverElement) {
        new bootstrap.Popover(popoverElement, {
            html: true // Enable HTML content
        });

        // Remove aria-hidden if present
        popoverElement.removeAttribute('aria-hidden');
    });
});

// Download table as Excel Sheet
document.getElementById('download_excel').addEventListener('click', function () {
    const table = document.getElementById('users-table');
    if (!table) {
        console.error("Table not found!");
        return;
    }

    // Convert table to SheetJS worksheet
    const worksheet = XLSX.utils.table_to_sheet(table, { raw: true });

    // Apply basic styling for borders and alignment
    const range = XLSX.utils.decode_range(worksheet['!ref']);

    for (let row = range.s.r; row <= range.e.r; row++) {
        for (let col = range.s.c; col <= range.e.c; col++) {
            const cellAddress = XLSX.utils.encode_cell({ r: row, c: col });
            if (!worksheet[cellAddress]) continue;

            // Process the cells with multiple bullet points
            let cellValue = worksheet[cellAddress].v || "";
            if (typeof cellValue === "string") {
                // Replace <br> tags with line breaks for Excel
                cellValue = cellValue.replace(/<br\s*\/?>/gi, "\n");
                worksheet[cellAddress].v = cellValue;
            }

            // Apply styling
            worksheet[cellAddress].s = {
                border: {
                    top: { style: "thin", color: { rgb: "000000" } },
                    bottom: { style: "thin", color: { rgb: "000000" } },
                    left: { style: "thin", color: { rgb: "000000" } },
                    right: { style: "thin", color: { rgb: "000000" } },
                },
                alignment: {
                    horizontal: "center",
                    vertical: "center",
                    wrapText: true, // Ensure multiline text
                },
            };
        }
    }

    // Dynamically adjust column widths
    const colWidths = [];
    for (let col = range.s.c; col <= range.e.c; col++) {
        let maxWidth = 10;  // Minimum width
        for (let row = range.s.r; row <= range.e.r; row++) {
            const cellAddress = XLSX.utils.encode_cell({ r: row, c: col });
            const cellValue = worksheet[cellAddress] && worksheet[cellAddress].v !== undefined ? worksheet[cellAddress].v.toString(): "";
            const cellLength = cellValue.length;
            maxWidth = Math.max(maxWidth, cellLength);
        }
        colWidths.push({ width: maxWidth + 2 });        // Add padding for better readability
    }

    worksheet['!cols'] = colWidths;     // Set column widths

    // Create workbook and add worksheet
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Users Table");

    // Export the workbook as Excel file
    XLSX.writeFile(workbook, "users_table.xlsx");
});

// Search Button Functionalities
document.getElementById('search-btn').addEventListener('click', function () {
        performSearch();
});

document.getElementById('search-input').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        performSearch();
    }
});

function performSearch() {
    const query = document.getElementById('search-input').value;

    // Redirect to the same page with the search query as a parameter
    window.location.href = `/database?query=${encodeURIComponent(query)}`;
}




