const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

function loadCSV(filePath) {
  return new Promise((resolve, reject) => {
    const results = [];
    fs.createReadStream(path.join(__dirname, 'data', filePath))
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', () => {
        resolve(results);
      });
  });
}

function parseDate(dateString) {
  // Adjust this function based on your date format
  return new Date(dateString);
}

function renderTable(data) {
  const tableContainer = document.getElementById('table-container');
  const table = document.createElement('table');

  // Create table header
  const header = table.createTHead();
  const headerRow = header.insertRow(0);

  const columns = Object.keys(data[0]);
  columns.forEach((col) => {
    const th = document.createElement('th');
    th.textContent = col;
    th.dataset.column = col;

    if (col.toLowerCase() === 'date') {
      th.style.cursor = 'pointer';
      th.addEventListener('click', () => {
        sortTableByDate(data, table);
      });
    }

    headerRow.appendChild(th);
  });

  // Create table body
  const tbody = document.createElement('tbody');
  data.forEach((row) => {
    const tr = document.createElement('tr');
    columns.forEach((col) => {
      const td = document.createElement('td');
      td.textContent = row[col];
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });

  table.appendChild(tbody);
  tableContainer.innerHTML = ''; // Clear previous content
  tableContainer.appendChild(table);
}

function sortTableByDate(data, table) {
  // Toggle sort direction
  if (!sortTableByDate.sortDirection || sortTableByDate.sortDirection === 'desc') {
    sortTableByDate.sortDirection = 'asc';
  } else {
    sortTableByDate.sortDirection = 'desc';
  }

  // Sort data
  data.sort((a, b) => {
    const dateA = parseDate(a.Date);
    const dateB = parseDate(b.Date);

    if (sortTableByDate.sortDirection === 'asc') {
      return dateA - dateB;
    } else {
      return dateB - dateA;
    }
  });

  // Re-render table with sorted data
  renderTable(data);

  // Update header classes
  const ths = document.querySelectorAll('th');
  ths.forEach((th) => {
    if (th.dataset.column === 'Date') {
      th.classList.remove('asc', 'desc');
      th.classList.add(sortTableByDate.sortDirection);
    }
  });
}

// Load the CSV data
loadCSV('actions.csv').then((data) => {
  renderTable(data);
});
