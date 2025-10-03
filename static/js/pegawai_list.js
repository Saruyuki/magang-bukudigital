document.addEventListener('DOMContentLoaded', () => {
    const table = document.getElementById('pegawaiTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const paginationContainer = document.getElementById('pagination');
    const searchInput = document.getElementById('searchInput');
    const filterColumnSelect = document.getElementById('filterColumn');
    const filterInput = document.getElementById('filterInput');

    const rowsPerPage = 20;
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
        const end = start + rowsPerPage;
        const pageRows = filteredRows.slice(start, end);
        
        if (pageRows.length === 0) {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            td.colSpan = table.querySelectorAll('thead th').length;
            td.textContent = 'Tidak ada data';
            tr.appendChild(td);
            tbody.appendChild(tr);
            return;
        }

        pageRows.forEach(row => tbody.appendChild(row));
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
        filteredRows = row.filter(row => {
            return Array.from(row.cells).some(td => td.innerText.toLowerCase().includes(searchTerm));
        });
    }

    filterColumnSelect.addEventListener('change', () => {
        if (filterColumnSelect.value) {
            filterInput.disabled = false;
            filterInput.value = '';
            filterInput.focus();
        } else {
            filterInput.disabled = true;
            filterInput.value = '';
        }
        applyFilter();
    });

    filterInput.addEventListener('input', () => {
        applyFilter();
    });

    searchInput.addEventListener('input', () => {
        applyFilter();
    })

    function applyFilter() {
        let tempRows = [...rows];

        const searchTerm = searchInput.value.trim().toLowerCase();
        if (searchTerm) {
            tempRows = tempRows.filter(row => {
                return Array.from(row.cells).some(td => td.innerText.toLowerCase().includes(searchTerm));
            });
        }

        const filterCol = filterColumnSelect.value;
        const filterVal = filterInput.value.trim().toLowerCase();
        if (filterCol && filterVal) {
            tempRows = tempRows.filter(row => {
                const cellVal = getCellValue(row, filterCol);
                return cellVal.includes(filterVal);
            });
        }

        filteredRows = tempRows;

        if (currentSort.column) {
            sortRows(currentSort.column, currentSort.direction);
        }

        currentPage = 1;
        renderTable();
    }

    renderTable();
})