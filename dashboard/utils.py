import re
import pdfplumber
from datetime import datetime, timedelta

def categorize_keperluan(keperluan_text):
    keperluan_text = keperluan_text.lower()
    for category, keywords in KEPERLUAN_CATEGORIES.items():
        if any(keyword in keperluan_text for keyword in keywords):
            return category
    return 'Lainnya'

def parse_date(text):
    bulan_map = {
        'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4,
        'Mei': 5, 'Juni': 6, 'Juli': 7, 'Agustus': 8,
        'September': 9, 'Oktober': 10, 'November': 11, 'Desember':12 
    }
    
    match = re.search(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', text)
    if not match:
        return None
    day, month_str, year = match.groups()
    month = bulan_map.get(month_str.capitalize())
    if not month:
        return None
    return datetime(int(year), month, int(day)).date()

def parse_surat_tugas(pdf_file):
    """
    Extract structured data from Surat Tugas PDF
    Returns a dict like:
    {
        'no_surat': str,
        'agenda': str,
        'tujuan': str,
        'start_date": date,
        'end_date': date,
        'pengurus': [('Nama', 'Jabatan'), ...]
    }
    """
    
    text = ''
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
            text += '\n'
    
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    joined = " ".join(lines)

    # --- Extract No Surat ---
    m_no = re.search(r'NO\s*[:\-]?\s*([A-Z0-9\/\.\-]+)', joined, re.IGNORECASE)
    no_surat = m_no.group(1).strip() if m_no else None

    # --- Extract Nama & Jabatan utama ---
    nama_utama = ''
    jabatan_utama = ''
    for i, line in enumerate(lines):
        if line.startswith('2 ') and ':' in line:
            nama_utama = line.split(':', 1)[1].strip()
        elif line.startswith('3 ') and ':' in line:
            jabatan_utama = line.split(':', 1)[1].strip()

    # --- Extract Agenda (Maksud perjalanan dinas) ---
    agenda = ""
    for i, line in enumerate(lines):
        if re.search(r"Maksud.*perjalanan.*dinas", line, re.IGNORECASE):
            collected = []

            # 1️⃣ check previous line (the text before '4 Maksud...')
            if i > 0 and not re.match(r"^\s*\d", lines[i - 1]):  # not a numbered section
                collected.append(lines[i - 1].strip())

            # 2️⃣ extract from current line (after ':')
            parts = line.split(":", 1)
            if len(parts) > 1:
                after_colon = parts[1].strip()
                if after_colon:
                    collected.append(after_colon)

            # 3️⃣ collect next lines until next numbered section
            for j in range(i + 1, len(lines)):
                if re.match(r"^\s*\d[.)]?\s", lines[j]):
                    break
                collected.append(lines[j].strip())

            # merge and clean spaces
            agenda = " ".join(collected).replace("  ", " ").strip()
            break


    # --- Extract Tujuan ---
    tujuan = ''
    for i, line in enumerate(lines):
        if re.match(r'^\s*6[.)]?\s', line):
            # Look ahead for "b." line or any that includes "Tempat tujuan"
            for j in range(i, len(lines)):
                if re.match(r'^\s*b[.)]?\s', lines[j].lower()):
                    # Get next non-empty line after this
                    if j + 1 < len(lines):
                        tujuan = lines[j + 1].strip()
                    else:
                        tujuan = lines[j].split(':')[-1].strip()
                        
                    if tujuan.lower().startswith('b.'):
                        tujuan = tujuan[2:].strip()
                    break
            break

    # --- Extract Tanggal ---
    start_date = None
    end_date = None
    for i, line in enumerate(lines):
        if re.search(r'Tanggal berangkat', line, re.IGNORECASE):
            start_date = parse_date(line.split(':')[-1])
            if not start_date and i + 1 < len(lines):
                start_date = parse_date(lines[i + 1])
        elif re.search(r'Tanggal harus', line, re.IGNORECASE):
            end_date = parse_date(line.split(':')[-1])
            if not end_date and i + 1 < len(lines):
                end_date = parse_date(lines[i + 1])

    # --- Extract Pendamping ---
    pendamping = []
    idx8 = None
    for i, line in enumerate(lines):
        if re.match(r'8[.)]?\s*(Nama Pendamping|Pendamping)', line, re.IGNORECASE):
            idx8 = i
            break

    if idx8 is not None:
        for j in range(idx8 + 1, len(lines)):
            l = lines[j]
            if re.match(r'^\d[.)]?\s', l) or l.startswith('9'):
                break
            # Match formats like "1. Alfin - Pengurus" or "Siti: Bendahara"
            m = re.match(r'\d*\.*\s*([A-Za-z\s\.]+)\s*[-:]\s*([A-Za-z\s&\./()]+)', l)
            if m:
                pendamping.append((m.group(1).strip(), m.group(2).strip()))
            else:
                if l and len(l.split()) > 1:
                    pendamping.append((l.strip(), ''))
    pengurus = [(nama_utama, jabatan_utama)] + pendamping

    return {
        'no_surat': no_surat,
        'agenda': agenda,
        'tujuan': tujuan,
        'start_date': start_date,
        'end_date': end_date,
        'pengurus': pengurus,
    }
    

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