document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("fotoModal");
  const fotoPreview = document.getElementById("fotoPreview");
  const fotoDateTime = document.getElementById("fotoDateTime");
  const fotoMapDiv = document.getElementById("fotoMap");
  const fotoCoord = document.getElementById("fotoCoord");

  let map = null;
  let marker = null;
  let defaultZoom = 15;

  modal.addEventListener("click", e => {
    if (e.target === modal) modal.classList.add("hidden");
  });



  window.showFotoModal = function (id, fotoUrl, lat, lon, datetime) {

    console.log("Showing foto modal with:", {id, fotoUrl, lat, lon, datetime});
    
    const latNum = parseFloat(lat.toString().replace(",",".")) || 0;
    const lonNum = parseFloat(lon.toString().replace(",",".")) || 0;

    fotoPreview.src = fotoUrl;
    fotoDateTime.textContent = datetime || "Tidak diketahui";
    fotoCoord.textContent = `Koordinat: ${latNum.toFixed(9)}, ${lonNum.toFixed(9)}`;
    modal.classList.remove("hidden");

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
