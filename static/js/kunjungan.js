document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("kunjungan-form");
    const photoInput = document.getElementById("foto_kunjungan");
    const cameraModal = document.getElementById("cameraModal");
    const openCameraBtn = document.getElementById("openCameraBtn");
    const captureBtn = document.getElementById("captureBtn");
    const video = document.getElementById("cameraPreview");
    const canvas = document.getElementById("snapshotCanvas");
    const photoPreview = document.getElementById("photoPreview");
    const latInput = document.getElementById("client_lat");
    const lonInput = document.getElementById("client_lon");
    const dtInput = document.getElementById("client_photo_dt");
    const modal = document.getElementById("successModal");

    // Hide modal initially
    if (modal) modal.style.display = "none";

    let stream;

    async function requestPermissions() {
    try {
        // Check and ask for camera permission
        const cameraStatus = await navigator.permissions.query({ name: 'camera' }).catch(() => null);
        if (cameraStatus && cameraStatus.state === 'denied') {
            showNotif("Akses kamera ditolak. Harap izinkan kamera di pengaturan browser Anda.");
            return false;
        }

        // Check and ask for location permission
        const geoStatus = await navigator.permissions.query({ name: 'geolocation' }).catch(() => null);
        if (geoStatus && geoStatus.state === 'denied') {
            showNotif("Akses lokasi ditolak. Harap izinkan lokasi di pengaturan browser Anda.");
            return false;
        }

        // Now request actual access to trigger permission popup if needed
        await navigator.mediaDevices.getUserMedia({ video: true });
        await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject, { enableHighAccuracy: true });
        });

        console.log("Permissions granted ✅");
        return true;

    } catch (err) {
        console.error("Permission request failed:", err);
        showNotif("Gagal meminta izin kamera atau lokasi. Harap periksa pengaturan browser Anda.");
        return false;
    }
}

    async function requestLocation() {
        if (!navigator.geolocation) {
            showNotif("Browser tidak mendukung GPS.");
            return;
        }

        const locStatus = document.getElementById("locationStatus")

        navigator.geolocation.getCurrentPosition(
            pos => {
                latInput.value = pos.coords.latitude.toFixed(9);
                lonInput.value = pos.coords.longitude.toFixed(9);
                dtInput.value = new Date().toISOString();

                if (locStatus) {
                    locStatus.textContent = `Lokasi: ${latInput.value}, ${lonInput.value}`;
                }

                console.log("Location captured:", latInput.value, lonInput.value);
            },
            err => {
                console.warn("Location denied:", err);
                showNotif("Tidak dapat mengambil lokasi. Harap aktifkan GPS.");
                if (locStatus) {
                    locStatus.textContent = "Gagal mengambil lokasi";
                }
            },
            { enableHighAccuracy: true, timeout: 10000 }
        );
    }
    
    openCameraBtn.addEventListener("click", async () => {
        const granted = await requestPermissions();
        if (!granted) return;
        
        cameraModal.classList.remove("hidden");
        await requestLocation();
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
        } catch (err) {
            showError("Tidak dapat mengakses kamera. Pastikan izin telah diberikan.");
            console.error(err);
        }
    })

    function closeCamera() {
        cameraModal.classList.add("hidden");
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    }

    cameraModal.addEventListener("click", e => {
        if (e.target === cameraModal) {
            closeCamera();
        }
    });

    captureBtn.addEventListener("click", async () => {
        if (!stream) return showError("Kamera tidak aktif.");

        const context = canvas.getContext("2d");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(async blob => {
            if (!blob) return showError("Gagal mengambil foto.");

            const dataUrl = canvas.toDataURL("image/png");
            photoPreview.src = dataUrl;
            photoPreview.style.display = "block";
            photoPreview.classList.remove("hidden");

            const file = new File([blob], "kunjungan.png", { type: "image/png" });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            photoInput.files = dataTransfer.files;
            
            closeCamera();
            console.log("Foto berhasil diambil");
        }, "image/png")

        
    });

    form.addEventListener("submit", async e => {
        e.preventDefault();

        const fd = new FormData(form);
        const photo = photoInput.files[0];
        if (!photo) {
            showNotif("Ambil foto kunjungan terlebih dahulu!");
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
                showNotif("Gagal mengirim form. Coba lagi.");
                console.error(data.errors || data.error);
            }
        } catch (err) {
            console.error("Network error:", err);
            showNotif("Terjadi kesalahan jaringan.");
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
});
