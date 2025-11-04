document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("kunjungan-form");
    const photoInput = document.getElementById("foto_kunjungan");
    const takePhotoBtn = document.getElementById("takePhotoBtn");
    const latInput = document.getElementById("client_lat");
    const lonInput = document.getElementById("client_lon");
    const dtInput = document.getElementById("client_photo_dt");
    const modal = document.getElementById("successModal");

    // Hide modal initially
    modal.style.display = "none";

    async function requestCamera() {
        try {
            if (navigator.mediaDevices?.getUserMedia) {
                await navigator.mediaDevices.getUserMedia({ video: true });
                console.log("Camera access granted");
            } else {
                console.warn("Browser does not support camera API");
            }
        } catch (err) {
            alert("Tidak dapat mengakses kamera. Harap izinkan akses kamera di browser Anda.");
        }
    }

    async function requestLocation() {
        if (!navigator.geolocation) {
            alert("Browser tidak mendukung GPS.");
            return;
        }

        const locStatus = document.getElementById("locationStatus")

        navigator.geolocation.getCurrentPosition(
            pos => {
                latInput.value = pos.coords.latitude;
                lonInput.value = pos.coords.longitude;
                dtInput.value = new Date().toISOString();

                if (locStatus) {
                    locStatus.textContent = `📍 Lokasi: ${pos.coords.latitude.toFixed(5)}, ${pos.coords.longitude.toFixed(5)}`;
                }

                console.log("Location captured:", latInput.value, lonInput.value);
            },
            err => {
                console.warn("Location denied:", err);
                alert("Tidak dapat mengambil lokasi. Harap aktifkan GPS.");
                if (locStatus) {
                    locStatus.textContent = "Gagal mengambil lokasi";
                }
            },
            { enableHighAccuracy: true, timeout: 10000 }
        );
    }

    takePhotoBtn.addEventListener("click", async () => {
        await requestCamera();
        await requestLocation();
        photoInput.click(); // open camera or file dialog
    });

    form.addEventListener("submit", async e => {
        e.preventDefault();

        const fd = new FormData(form);
        const photo = photoInput.files[0];
        if (!photo) {
            alert("Ambil foto kunjungan terlebih dahulu!");
            return;
        }
        fd.append("foto_kunjungan", photo);

        // Submit via AJAX
        try {
            const res = await fetch(window.location.href, {
                method: "POST",
                body: fd,
            });
            const data = await res.json();
            if (data.success) {
                modal.style.display = "flex";
                form.reset();
            } else {
                alert("Gagal mengirim form. Coba lagi.");
                console.error(data.errors || data.error);
            }
        } catch (err) {
            console.error("Network error:", err);
            alert("Terjadi kesalahan jaringan.");
        }
    });

    // Modal close behavior
    modal.addEventListener("click", e => {
        if (e.target === modal) {
            modal.style.display = "none";
            window.location.href = redirectAfterSubmit;
        }
    });
    const okBtn = document.getElementById("modalOkBtn");
    if (okBtn) okBtn.addEventListener("click", () => {
        modal.style.display = "none";
        window.location.href = redirectAfterSubmit;
    });

    photoInput.addEventListener('change', () => {
        const file = photoInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = e => {
                const img = document.getElementById('photoPreview');
                img.src = e.target.result;
                img.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    })
    
});
