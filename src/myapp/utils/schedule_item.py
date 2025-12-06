from dataclasses import dataclass
from myapp.utils.struct_pengajar import Pengajar
from myapp.utils.struct_matakuliah import MataKuliah

# --- DEFINISI INTERNAL MODEL (Untuk Algoritma) ---


@dataclass
class ScheduleItem:
    """
    Representasi internal untuk satu unit jadwal (Kelas) dalam algoritma SA.
    Menghubungkan MataKuliah, Kelas spesifik, dan Pengajar.
    """

    uid: int  # Unique ID untuk algoritma
    mk: MataKuliah  # Object MataKuliah (Struct)
    kelas_code: str  # Kode kelas: 'A', 'B', 'C'
    pengajar: Pengajar  # Object Pengajar (Struct)

    # Variabel Keputusan (Decision Variables)
    timeslot_index: int  # Index pointer ke list global 'valid_timeslots'
    ruangan_id: int | None  # ID Ruangan (dari struct Ruangan)
    is_daring: bool  # Status online/offline
