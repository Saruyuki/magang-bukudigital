console.log('surat_upload.js loaded');

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('uploadModal');
    const openBtn = document.getElementById('openUploadModal');
    const form = document.getElementById('uploadForm');
    const tableBody = document.getElementById('listTableBody');
    const resultBox = document.getElementById('uploadResult');
    const previewBtn = document.getElementById('previewBtn');

    openBtn.addEventListener('click', () => modal.classList.remove('hidden'));

    modal.addEventListener('click', e => {
        if (e.target === modal) modal.classList.add('hidden');
    });

    async function processSurat(preview = false) {
        resultBox.textContent = preview
        ? "Menganalisis surat (preview)"
        : "Mengupload dan memproses surat...";
        
        const formData = new FormData(form);
        const url = `/surat/upload/${preview ? '?preview=true' : ''}`;

        try {
            console.log("Submitting to:", url)
            const res = await fetch(url, {
                method: "POST",
                headers: { "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value },
                body: formData
            });

            const data = await res.json();
            console.log("Server Response:", data);

            if (!data.success) {
                resultBox.innerHTML = `<p class="text-red-600 font-semibold">${data.error || 'Gagal memproses surat.'}.</p>`;
                return;
            }

            if (data.mode === "preview") {
                const parsed = data.parsed;
                const pengurusList = parsed.pengurus.map(p => `<li>${p[0]} - ${p[1]}</li>`).join('');
                resultBox.innerHTML = `
                    <div class="text-gray-700 text-sm space-y-1">
                        <p><b>No Surat:</b> ${parsed.no_surat}</p>
                        <p><b>Agenda:</b> ${parsed.agenda}</p>
                        <p><b>Tujuan:</b> ${parsed.tujuan}</p>
                        <p><b>Tanggal:</b> ${parsed.start_date || '-'} -> ${parsed.end_date || '-'} </p>
                        <p><b>Daftar Pengurus:</b></p>
                        <ul class="list-disc pl-5">${pengurusList}</ul>
                    </div>
                `;
                return;
            }

            resultBox.innerHTML = `<p class="text-green-600 font-semibold">Surat berhasil diupload.<br>${data.created} form kehadiran dibuat.</p>`;

            const now = new Date();
            const formattedDate = now.toLocaleString('id-ID', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit',});
            const newRow =`
                <tr>
                    <td>${formData.get('no_surat')}</td>
                    <td>${formattedDate}</td>
                    <td>${window.currentUserName}</td>
                    <td>${data.created}</td>
                </tr>`;
            
            const fullBody = document.getElementById('listTableBodyFull');
            fullBody.insertAdjacentHTML('afterbegin', newRow);

            if (typeof renderTable === 'function') {
                renderTable()
            }

            setTimeout(() => {
                modal.classList.add('hidden');
                resultBox.textContent = '';
                form.reset();
            }, 1200);
                

        } catch (err) {
            console.error(err);
            resultBox.innerHTML = `<p class="text-red-600 font-semibold">Kesalahan jaringan, coba lagi.</p>`;
        }
    }

    previewBtn.addEventListener('click', (e) => {
        e.preventDefault();
        processSurat(true)
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        processSurat(false);
    });
});