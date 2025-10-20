document.addEventListener("DOMContentLoaded", function () {
    const ctxProvinsi = document.getElementById("provinsiChart").getContext("2d");
    new Chart(ctxProvinsi, {
        type: "bar",
        data: {
            labels: provinsiLabels,
            datasets: [{
                label: "Jumlah Pengunjung",
                data: provinsiData,
                backgroundColor: "#42a5f5"
            }]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
                legend: { display: false }
            }
        }
    });

    const ctxKeperluan = document.getElementById("keperluanChart").getContext("2d");
    new Chart(ctxKeperluan, {
        type: "pie",
        data: {
            labels: keperluanLabels,
            datasets : [{
                data: keperluanData,
                backgroundColor: ["#66bb6a", "#ef5350", "#ffa726", "#29b6f6", "#ab47bc"]
            }]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
        }
    });
})