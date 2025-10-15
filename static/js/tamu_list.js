document.addEventListener('DOMContentLoaded', () => {
    const table = document.getElementById('tamuTable');
    const fullTbody = document.getElementById('tamuTableBodyFull');
    const tbody = document.getElementById('tamuTableBody');
    const rows = Array.from(fullTbody.querySelectorAll('tr'));
    const paginationContainer = document.getElementById('pagination');
    const searchInput = document.getElementById('searchInput');
    const filterColumnSelect = document.getElementById('filterColumn');
    const rowsPerPageSelect = document.getElementById('rowsPerPageSelect');
    const totalRecordsSpan = document.getElementById('totalRecords');

    let rowsPerPage = rowsPerPageSelect.value === 'all' ? Infinity : parseInt(rowsPerPageSelect.value, 10);
    let currentPage = 1;
    let currentSort = { column: null, direction: null};
    let filteredRows =[...rows];

    function getCellValue(row, column) {
        const headers = Array.from(table.querySelectorAll('thead th'));
        const index = headers.findIndex(h => h.dataset.column === column);
        return row.cells[index].innerText.trim().toLowerCase() || '';
    }

    function sortRows(column, direction) {
        filteredRows.sort((a, b) => {
            let valA = getCellValue(a, column);
            let valB = getCellValue(b, column);

            if (column === 'tanggal_kunjungan') {
                valA = Date.parse(valA);
                valB = Date.parse(valB);
            }

            if (valA < valB) return direction === 'asc' ? -1 : 1;
            if (valA > valB) return direction === 'asc' ? 1 : -1;
            return 0;
        });
    }

    function renderTable() {
        tbody.innerHTML = '';

        const start = (currentPage - 1) * rowsPerPage;
        const end = rowsPerPage === Infinity ? filteredRows.length : start + rowsPerPage;
        const pageRows = filteredRows.slice(start, end);
        
        if (pageRows.length === 0) {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            td.colSpan = table.querySelectorAll('thead th').length;
            td.textContent = 'Tidak ada data';
            tr.appendChild(td);
            tbody.appendChild(tr);
            return;
        } else {
            pageRows.forEach(row => tbody.appendChild(row.cloneNode(true)));
        }
    
        updateTotalRecords();
        renderPagination();
    }

    function renderPagination() {
        paginationContainer.innerHTML = '';
        const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
        if (totalPages <= 1 ) return;

        const prevBtn = document.createElement('button');
        prevBtn.textContent ='<'
        prevBtn.disabled = currentPage === 1;
        prevBtn.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                renderTable();
            }
        });
        paginationContainer.appendChild(prevBtn);

        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement('button');
            btn.textContent = i;
            if ( i === currentPage) btn.classList.add('active');
            btn.addEventListener('click', () => {
                currentPage = i;
                renderTable();
            });
            paginationContainer.appendChild(btn);
        }

        const nextBtn = document.createElement('button');
        nextBtn.textContent = '>';
        nextBtn.disabled = currentPage === totalPages;
        nextBtn.addEventListener('click', () => {
            if (currentPage < totalPages) {
                currentPage++;
                renderTable()
            }
        });
        paginationContainer.appendChild(nextBtn);
    }

    function clearSortClasses() {
        table.querySelectorAll('th.sortable').forEach(th => {
            th.classList.remove('sorted-asc', 'sorted-desc');
        });
    }

    table.querySelectorAll('th.sortable').forEach(th => {
        th.addEventListener('click', () => {
            const column = th.dataset.column;
            let direction = 'asc';

            if (currentSort.column === column && currentSort.direction === 'asc') {
                direction = 'desc';
            }

            currentSort = { column, direction };
            clearSortClasses();
            th.classList.add(direction === 'asc' ? 'sorted-asc' : 'sorted-desc');

            sortRows(column, direction);
            currentPage = 1;
            renderTable();
        });
    });

    function applySearchFilter() {
        const searchTerm = searchInput.value.trim().toLowerCase();
        if (!searchTerm) {
            filteredRows = [...rows];
            return;
        }
        filteredRows = rows.filter(row => {
            return Array.from(row.cells).some(td => td.innerText.toLowerCase().includes(searchTerm));
        });
    }

    filterColumnSelect.addEventListener('change', () => {
        applyFilter();
    });

    searchInput.addEventListener('input', () => {
        applyFilter();
    })

    function applyFilter() {
        const searchTerm = searchInput.value.trim().toLowerCase();
        const filterCol = filterColumnSelect.value;

        if (!searchTerm) {
            filteredRows = [...rows];
        } else if (!filterCol) {
            filteredRows = rows.filter(row => {
                return Array.from(row.cells).some(td => td.innerText.toLowerCase().includes(searchTerm));
            }); 
        } else {
            filteredRows = rows.filter(row => { 
                const cellVal = getCellValue(row, filterCol);
                return cellVal.includes(searchTerm);
            })
        }

        if (currentSort.column) {
            sortRows(currentSort.column, currentSort.direction);
        }

        currentPage = 1;
        renderTable();
    }

    function updateTotalRecords() {
        totalRecordsSpan.textContent = filteredRows.length;
    }

    rowsPerPageSelect.addEventListener('change', () => {
        const value = rowsPerPageSelect.value;
        rowsPerPage = value === 'all' ? filteredRows.length : parseInt (value, 10);
        currentPage = 1;
        renderTable();
    })

    renderTable();
})