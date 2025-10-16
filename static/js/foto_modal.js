document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("fotoModal");
  const closeBtn = document.getElementById("closeFotoModal");
  const fotoPreview = document.getElementById("fotoPreview");
  const fotoDateTime = document.getElementById("fotoDateTime");
  const fotoMapDiv = document.getElementById("fotoMap");
  let map = null;
  let marker = null;
  let defaultZoom = 15;

  closeBtn.addEventListener("click", () => modal.classList.add("hidden"));
  modal.addEventListener("click", e => {
    if (e.target === modal) modal.classList.add("hidden");
  });

  window.showFotoModal = function (id, fotoUrl, lat, lon, datetime) {
    fotoPreview.src = fotoUrl;
    fotoDateTime.textContent = datetime || "Tidak diketahui";
    modal.classList.remove("hidden");

    const latNum = parseFloat(lat) || 0;
    const lonNum = parseFloat(lon) || 0;

    if (!map) {
      map = L.map(fotoMapDiv, {
        zoomControl: true,
        scrollWheelZoom: true,
        doubleClickZoom: true,
        minZoom: defaultZoom,
        maxZoom: 19,
      }).setView([latNum, lonNum], defaultZoom);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '',
      }).addTo(map);

      marker = L.marker([latNum, lonNum]).addTo(map).bindPopup("Lokasi Foto");
    } else {
      map.setView([latNum, lonNum], defaultZoom);
      if (marker) marker.setLatLng([latNum, lonNum]);
      else marker = L.marker([latNum, lonNum]).addTo(map);
    }

    setTimeout(() => map.invalidateSize(), 200);
  };

  window.isiForm = function (kunjunganId) {
      window.location.href = `/kunjungan/${kunjunganId}/`;
  };
});
