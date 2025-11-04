document.addEventListener('DOMContentLoaded', () => {
    const table = document.getElementById('listTable');
    const fullTbody = document.getElementById('listTableBodyFull');
    const tbody = document.getElementById('listTableBody');

    if (!table || !fullTbody || !tbody) {
        console.warn("⚠️ suratTableBodyFull or table not found in DOM.");
        return;
    }

    const rows = Array.from(fullTbody.querySelectorAll('tr'));
    const paginationContainer = document.getElementById('pagination');
    const searchInput = document.getElementById('searchInput');
    const filterColumnSelect = document.getElementById('filterColumn');
    const rowsPerPageSelect = document.getElementById('rowsPerPageSelect');
    const totalRecordsSpan = document.getElementById('totalRecords');

    let rowsPerPage = rowsPerPageSelect?.value === 'all' ? Infinity : parseInt(rowsPerPageSelect?.value, 10);
    let currentPage = 1;
    let currentSort = { column: null, direction: null};
    let filteredRows =[...rows];

    console.log(`table_list.js initialized with ${rows.length} rows`);

    function getCellValue(row, column) {
        const headers = Array.from(table.querySelectorAll('thead th'));
        const index = headers.findIndex(h => h.dataset.column === column);
        return row.cells[index].innerText.trim().toLowerCase() || '';
    }

    function sortRows(column, direction) {
        filteredRows.sort((a, b) => {
            let valA = getCellValue(a, column);
            let valB = getCellValue(b, column);

            if (['tanggal_kunjungan', 'created_at', 'tanggal_masuk'].includes(column)) {
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

    if (filterColumnSelect) filterColumnSelect.addEventListener('change', () => {
        applyFilter();
    });

    if (searchInput) searchInput.addEventListener('input', () => {
        applyFilter();
    })

    function applyFilter() {
        const searchTerm = searchInput?.value.trim().toLowerCase();
        const filterCol = filterColumnSelect?.value;

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

    if (rowsPerPageSelect) rowsPerPageSelect.addEventListener('change', () => {
        const value = rowsPerPageSelect?.value;
        rowsPerPage = value === 'all' ? filteredRows.length : parseInt (value, 10);
        currentPage = 1;
        renderTable();
    })

    renderTable();

    document.addEventListener('click', async (e) => {
        const row = e.target.closest('tr[data-id]');
        if (!row) return;
        const suratId = row.dataset.id;

        if (e.target.classList.contains('show-btn')) {
            const fileUrl = e.target.dataset.file;
            if (fileUrl) window.open(fileUrl, '_blank');
        }

        if (e.target.classList.contains('edit-btn')) {
            const currentNo = row.cells[0].innerText.trim();
            const newNo = prompt("Edit Nomor Surat:", currentNo);
            if (!newNo || newNo === currentNo) return;

            const res = await fetch(`/surat/${suratId}/edit`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `no_surat=${encodeURIComponent(newNo)}`
            });
            const data = await res.json();
            if (data.success) {
                row.cells[0].innerText = data.no_surat;
                showNotif('Nomor surat berhasil diperbarui');
            } else {
                showNotif(data.error || 'Gagal memperbarui no surat.');
            }
        }

        if (e.target.classList.contains('delete-btn')) {
            showConfirm("Hapus Surat Ini?", async () => {
                const res = await fetch(`/surat/${suratId}/delete`, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value },
                });
                const data = await res.json()
                if (data.success) {
                    row.remove();
                    showNotif('Surat berhasil dihapus.');
                } else {
                    showNotif('Gagal menghapus surat.');
                }
            });
        }
    });
})