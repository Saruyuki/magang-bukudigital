import re
import pdfplumber
from datetime import datetime, timedelta

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
            
    no_surat = None
    m_no = re.search(r'No\.?\s*[:\-]?\s*([A-Z0-9)\/\.\-]+)', text)
    if m_no: 
        no_surat = m_no.group(1).strip()
        
    agenda = ''
    m_agenda = re.search(r'4\.\s*(.*?)\n', text)
    if m_agenda:
        agenda = m_agenda.group(1).strip()
        
    tujuan = ''
    m_tujuan = re.search(r'6b\.\s*(.*?\n)', text)
    if m_tujuan:
        m_tujuan = m_tujuan.group(1).strip()
        
    start_date = None
    end_date = None
    m_start = re.search(r'7b\.\s*(.*?\n)', text)
    m_end = re.search(r'7c\.\s*(.*?\n)', text)
    if m_start:
        start_date = parse_date(m_start.group(1))
    if m_end:
        end_date = parse_date(m_end.group(1))
        
    nama_utama = ''
    jabatan_utama = ''
    m_nama = re.search(r'2\.\s*(.*?\n)', text)
    m_jabatan = re.search(r'3\.\s*(.*?\n)', text)
    if m_nama:
        nama_utama = m_nama.group(1).strip()
    if m_jabatan:
        jabatan_utama = m_jabatan.group(1).strip()
        
    pendamping = []
    m8 = re.search(r'8\.\s*(.*?\n)', text, re.DOTALL)
    if m8:
        lines = [l.strip() for l in m8.group(1).split('\n') if l.strip()]
        for line in lines:
            parts = re.split(r'[---:]', line, maxsplit=1)
            if len(parts) == 2:
                pendamping.append((parts[0].strip(), parts[1].strip()))
            else :
                pendamping.append((line.strip(), ''))
    
    pengurus = [(nama_utama, jabatan_utama)] + pendamping
    
    return {
        'no_surat': no_surat,
        'agenda': agenda,
        'tujuan': tujuan,
        'start_date': start_date,
        'end_date': end_date,
        'pengurus': pengurus,
    }
    
