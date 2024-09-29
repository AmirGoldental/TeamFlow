
function read_table(filePath) {
    // Fetch the file from the given path
    fetch(filePath)
    .then(response => {
        if (!response.ok) {
            throw new Error('File read error');
        }
        return response.text();
    })
    .then(csvData => {
        return parseCSVData(csvData);
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
    function parseCSVData(csvData) {
        let creationDateIndex = -1;
        let csvRows = [];

        const rows = csvData.split('\n').map(header => header.trim());
        // Get headers and find "Creation Date" index
        const headers = rows[0].split(',');
        creationDateIndex = headers.indexOf("Creation Date");

        let tableHTML = '<tr>';
        headers.forEach(header => {
            tableHTML += `<th>${header.trim()}</th>`;
        });
        tableHTML += '</tr>';

        // Get rows
        rows.slice(1).forEach(row => {
            if (row.trim() !== '') {
                const columns = row.split(',');
                csvRows.push(columns); // Store each row as an array
                tableHTML += '<tr>';
                columns.forEach(column => {
                    tableHTML += `<td>${column.trim()}</td>`;
                });
                tableHTML += '</tr>';
            }
        });

        // Set table content
        //document.getElementById('csvTable').innerHTML = tableHTML;
        return csvRows;
    }
}
let csvRows = read_table('data/actions.csv');
console.log(csvRows)