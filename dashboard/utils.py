PROVINCE_NAMES = [
    'Nanggroe Aceh Darussalam', 'Sumatera Utara', 'Sumatera Selatan', 'Sumatera Barat', 'Bengkulu', 'Riau', 
    'Kepulauan Riau', 'Jambi', 'Lampung', 'Bangka Belitung', 'Kalimantan Barat', 'Kalimantan Timur',
    'Kalimantan Selatan', 'Kalimantan Tengah', 'Kalimantan Utara',  'Banten', 'DKI Jakarta',
    'Jawa Barat', 'Jawa Tengah', 'DI Yogyakarta', 'Jawa Timur', 'Bali', 'Nusa Tenggara Timur',
    'Nusa Tenggara Barat', 'Gorontalo', 'Sulawesi Barat', 'Sulawesi Tengah', 'Sulawesi Utara',
    'Sulawesi Tenggara', 'Sulawesi Selatan', 'Maluku', 'Maluku Utara', 'Papua Barat', 'Papua', 
    'Papua Tengah', 'Papua Pegunungan', 'Papua Selatan', 'Papua Barat Daya'
]

INDO_PROVINCES = [(prov, prov) for prov in PROVINCE_NAMES]

PROVINCE_ACRONYMS = {
    'Nanggroe Aceh Darussalam' : 'Aceh',
    'Sumatera Utara': 'Sumut',
    'Sumatera Selatan': 'Sumsel',
    'Sumatera Barat': 'Sumbar',
    'Bengkulu': 'Bengkulu',
    'Riau': 'Riau', 
    'Kepulauan Riau': 'Kepri',
    'Jambi': 'Jambi',
    'Lampung': 'Lampung',
    'Bangka Belitung': 'Babel',
    'Kalimantan Barat': 'Kalbar',
    'Kalimantan Timur': 'Kaltim',
    'Kalimantan Selatan': 'Kalsel',
    'Kalimantan Tengah': 'Kalteng',
    'Kalimantan Utara': 'Kaltara',
    'Banten': 'Banten',
    'DKI Jakarta': 'DKI Jakarta',
    'Jawa Barat': 'Jabar',
    'Jawa Tengah': 'Jateng',
    'DI Yogyakarta': 'DIY',
    'Jawa Timur': 'Jatim',
    'Bali': 'Bali',
    'Nusa Tenggara Timur': 'NTT',
    'Nusa Tenggara Barat': 'NTB',
    'Gorontalo': 'Gorontalo',
    'Sulawesi Barat': 'Sulbar',
    'Sulawesi Tengah': 'Sulteng',
    'Sulawesi Utara': 'Sulut',
    'Sulawesi Tenggara': 'Sultra',
    'Sulawesi Selatan': "Sulsel",
    'Maluku': 'Maluku',
    'Maluku Utara': 'Maluku Utara',
    'Papua Barat':'Pabar',
    'Papua': 'Papua', 
    'Papua Tengah': 'Pateng',
    'Papua Pegunungan': 'Papua Pegunungan',
    'Papua Selatan': 'Pasel',
    'Papua Barat Daya': 'Papua Barat Daya'
}

INDONESIAN_PROVINCES = [
    (prov, label, PROVINCE_ACRONYMS.get(prov, 'N/A'))
    for prov, label in INDO_PROVINCES
]

KEPERLUAN_CATEGORIES = {
    'Kunjungan Kerja': ['kerja', 'meeting', 'rapat', 'bisnis', 'proyek', 'dinas'],
    'Kunjungan Pribadi': ['pribadi', 'teman', 'keluarga', 'sosial', 'silaturahmi'],
    'Pengiriman Barang': ['pengiriman', 'barang', 'paket', 'logistik', 'kurir'],
    'Layanan Umum': ['umum', 'layanan', 'informasi', 'bantuan', 'konsultasi'],
    'Kunjungan Resmi': ['resmi', 'pemerintah', 'delegasi', 'diplomatik', 'kunjungan'],
    'Pertemuan' : ['pertemuan', 'diskusi', 'seminar', 'workshop', 'pelatihan'],
    'Lainnya': []
}

def categorize_keperluan(keperluan_text):
    keperluan_text = keperluan_text.lower()
    for category, keywords in KEPERLUAN_CATEGORIES.items():
        if any(keyword in keperluan_text for keyword in keywords):
            return category
    return 'Lainnya'