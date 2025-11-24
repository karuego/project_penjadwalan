import os
import sqlite3

# from .schedule_generator import ScheduleGenerator
# from .waktu_util import TimeSlotManager

DB_FILE: str = "database.sqlite3.db"

class Database:
    def __init__(self) -> None:
        if not self.is_exist():
            self.init_database()

    def init_database(self) -> None:
        """Initialize database dengan tabel yang diperlukan"""

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Tabel untuk menyimpan timeslots
            _ = cursor.execute("""
                CREATE TABLE IF NOT EXISTS timeslots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hari INTEGER NOT NULL,
                    mulai TEXT NOT NULL,
                    selesai TEXT NOT NULL,
                    UNIQUE(hari, mulai, selesai)
                )
            """)

            _ = cursor.execute("""
                CREATE TABLE pengajar (
                    id TEXT PRIMARY KEY NOT NULL,
                    nama TEXT NOT NULL,
                    jenis TEXT NOT NULL DEFAULT 'dosen',
                    preferensi_waktu TEXT
                )
            """)

            _ = cursor.execute("""
                CREATE TABLE mata_kuliah (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    semester INTEGER NOT NULL
                )
            """)

            _ = cursor.execute("""
                CREATE TABLE ruangan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL UNIQUE,
                    jenis TEXT NOT NULL DEFAULT 'teori'
                )
            """)

            _ = cursor.execute("""
                CREATE TABLE komponen_mk (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mata_kuliah_id INTEGER NOT NULL,
                    nama_komponen TEXT NOT NULL,
                    durasi_blok INTEGER NOT NULL,
                    jenis TEXT NOT NULL DEFAULT 'teori',
                    jumlah_kelas INTEGER NOT NULL,
                    jumlah_sesi_praktikum INTEGER NOT NULL DEFAULT 1,
                    FOREIGN KEY (mata_kuliah_id) REFERENCES mata_kuliah(id)
                )
            """)

            _ = cursor.execute("""
                CREATE TABLE pengampu (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pengajar_id INTEGER,
                    komponen_mk_id INTEGER NOT NULL,
                    FOREIGN KEY (pengajar_id) REFERENCES pengajar(id),
                    FOREIGN KEY (komponen_mk_id) REFERENCES komponen_mk(id)
                )
            """)

            _ = cursor.execute("""
                CREATE TABLE jadwal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    komponen_mk_id INTEGER NOT NULL,
                    pengajar_id INTEGER NOT NULL,
                    kelas CHAR NOT NULL,
                    sesi_ke INTEGER NOT NULL,
                    waktu_id_start INTEGER NOT NULL,
                    durasi_blok INTEGER NOT NULL,
                    ruangan_id INTEGER NULL,
                    daring BOOLEAN NOT NULL DEFAULT FALSE,
                    FOREIGN KEY (komponen_mk_id) REFERENCES komponen_mk(id),
                    FOREIGN KEY (pengajar_id) REFERENCES pengajar(id),
                    FOREIGN KEY (waktu_id_start) REFERENCES waktu(id)
                )
            """)

            conn.commit()

    def get_connection(self) -> sqlite3.Connection:
        """Mendapatkan koneksi database"""
        return sqlite3.connect(DB_FILE)

    def is_exist(self) -> bool:
        """Cek apakah file database sudah ada"""
        return os.path.exists(DB_FILE)
