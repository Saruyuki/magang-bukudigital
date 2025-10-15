$(document).ready(function() {
    const form = $("#kunjungan-form");
    const $modal = $('#successModal');
    $modal.hide();

    form.on ("submit", function(e) {
        e.preventDefault();
        const fd = new FormData(this);
        const photo = $("#foto_kegiatan")[0].files[0];
        if (photo) fd.append("foto_kegiatan", photo);

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    fd.append("client_lat", pos.coords.latitude);
                    fd.append("client_lon", pos.coords.longitude);
                    fd.append("client_photo_dt", new Date().toISOString());
                    sendForm(fd);
                },
                () => sendForm(fd),
                { enabledHighAccuracy: true, timeout: 10000}
            );
        } else sendForm(fd);
    });

    function sendForm(fd) {
        $.ajax({
            url:window.location.href,
            type: "POST",
            data: fd,
            processData: false,
            contentType: false,
            success: (res) => {
                if (res.success) {
                    $modal.show();
                    form[0].reset();
                } else alert("Gagal menyimpan data");  
            },
            error: () => alert("Terjadi kesalahan"),
        });
    }
});