CsvToHtmlTable.init({
    csv_path: "/data/raw/il-solar-installers-il-2025-08.csv",
    element: "installers-table",
    allow_download: true,
    csv_options: {
        separator: ",",
        delimiter: '"'
    },
    datatables_options: {
        paging: false,
        info: false,
        searching: true,
        ordering: true,
        order: [[0, 'asc']]
    },
});

CsvToHtmlTable.init({
    csv_path: "/data/raw/il-solar-installers-by-county-2025-08.csv",
    element: "installers-county-table",
    allow_download: true,
    csv_options: {
        separator: ",",
        delimiter: '"'
    },
    datatables_options: {
        paging: false,
        info: false,
        searching: true,
        ordering: true,
        order: [[0, 'asc'], [3, 'desc']]
    },
});