from dataclasses import dataclass


@dataclass
class Ruangan:
    id: int
    nama: str
    jenis: str  # 'teori' atau 'praktek'


@dataclass
class Dosen:
    id: int
    nama: str


@dataclass
class MataKuliah:
    id: int
    nama: str
    semester: int
    jumlah_kelas: int
    jenis: str  # 'teori' atau 'praktek'


@dataclass
class Waktu:
    id: int
    hari: str
    jam_mulai: str
    jam_selesai: str


@dataclass
class Pengampu:
    mata_kuliah_id: int
    dosen_id: int


@dataclass
class PreferensiDosen:
    dosen_id: int
    waktu_id: int
    hindari: bool = True


@dataclass
class JadwalItem:
    """Merepresentasikan satu entri dalam jadwal akhir."""

    mata_kuliah_id: int
    kelas: str  # 'A', 'B', dst.
    dosen_id: int
    waktu_id: int
    ruangan_id: int
    # Menambahkan informasi tambahan untuk memudahkan evaluasi
    semester: int
    jenis_mk: str  # 'teori' atau 'praktek'
