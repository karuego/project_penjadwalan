import sqlite3

from .struktur import Ruangan, Dosen, Waktu, MataKuliah, Pengampu, PreferensiDosen

DB_FILE = "jadwal.db"


class DatabaseManager:
    def __init__(self, db_path: str = DB_FILE) -> None:
        self.db_path: str = db_path
        # self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor: sqlite3.Cursor = conn.cursor()

            _ = cursor.execute("")
            _ = cursor.execute("")

            cursor.commit()

    def get_connection(self):
        return sqlite3.connect(self.db_path)


def setup(db_name: str = DB_FILE):
    """
    Membuat dan mengisi database SQLite dengan data awal jika belum ada.
    Fungsi ini bersifat idempoten, aman untuk dijalankan berkali-kali.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Membuat Tabel
    _ = cursor.executescript("""
        CREATE TABLE IF NOT EXISTS ruangan (
            id INTEGER PRIMARY KEY,
            nama TEXT UNIQUE NOT NULL,
            jenis TEXT NOT NULL CHECK(jenis IN ('teori', 'praktek'))
        );
        CREATE TABLE IF NOT EXISTS dosen (
            id INTEGER PRIMARY KEY,
            nama TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS mata_kuliah (
            id INTEGER PRIMARY KEY,
            nama TEXT NOT NULL,
            semester INTEGER NOT NULL,
            jumlah_kelas INTEGER NOT NULL,
            jenis TEXT NOT NULL CHECK(jenis IN ('teori', 'praktek'))
        );
        CREATE TABLE IF NOT EXISTS waktu (
            id INTEGER PRIMARY KEY,
            hari TEXT NOT NULL,
            jam_mulai TEXT NOT NULL,
            jam_selesai TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS pengampu (
            id INTEGER PRIMARY KEY,
            mata_kuliah_id INTEGER NOT NULL,
            dosen_id INTEGER NOT NULL,
            FOREIGN KEY (mata_kuliah_id) REFERENCES mata_kuliah(id),
            FOREIGN KEY (dosen_id) REFERENCES dosen(id)
        );
        CREATE TABLE IF NOT EXISTS preferensi_dosen (
            id INTEGER PRIMARY KEY,
            dosen_id INTEGER NOT NULL,
            waktu_id INTEGER NOT NULL,
            hindari BOOLEAN NOT NULL DEFAULT 1,
            FOREIGN KEY (dosen_id) REFERENCES dosen(id),
            FOREIGN KEY (waktu_id) REFERENCES waktu(id)
        );
    """)

    # Data Sampel untuk dimasukkan ke DB
    ruangan_data = [
        (1, "R-101", "teori"),
        (2, "R-102", "teori"),
        (3, "Lab-Kom A", "praktek"),
        (4, "Lab-Kom B", "praktek"),
    ]
    dosen_data = [(1, "Dr. Budi"), (2, "Dr. Ani"), (3, "Dr. Candra")]
    waktu_data = [
        (1, "Senin", "08:00", "10:00"),
        (2, "Senin", "10:00", "12:00"),
        (3, "Senin", "13:00", "15:00"),
        (4, "Senin", "15:00", "17:00"),
        (5, "Selasa", "08:00", "10:00"),
        (6, "Selasa", "10:00", "12:00"),
        (7, "Selasa", "13:00", "15:00"),
        (8, "Selasa", "15:00", "17:00"),
    ]
    mata_kuliah_data = [
        (1, "Basis Data", 3, 2, "teori"),
        (2, "Praktikum Basis Data", 3, 2, "praktek"),
        (3, "Kecerdasan Buatan", 5, 1, "teori"),
        (4, "Jaringan Komputer", 5, 1, "teori"),
    ]
    pengampu_data = [(1, 1, 1), (2, 2, 1), (3, 3, 2), (4, 4, 3)]
    preferensi_data = [(1, 2, 1, 1), (2, 3, 8, 1)]

    # Mengisi data menggunakan INSERT OR IGNORE agar tidak error jika data sudah ada
    _ = cursor.executemany(
        "INSERT OR IGNORE INTO ruangan (id, nama, jenis) VALUES (?,?,?)", ruangan_data
    )
    _ = cursor.executemany(
        "INSERT OR IGNORE INTO dosen (id, nama) VALUES (?,?)", dosen_data
    )
    _ = cursor.executemany(
        "INSERT OR IGNORE INTO waktu (id, hari, jam_mulai, jam_selesai) VALUES (?,?,?,?)",
        waktu_data,
    )
    _ = cursor.executemany(
        "INSERT OR IGNORE INTO mata_kuliah (id, nama, semester, jumlah_kelas, jenis) VALUES (?,?,?,?,?)",
        mata_kuliah_data,
    )
    _ = cursor.executemany(
        "INSERT OR IGNORE INTO pengampu (id, mata_kuliah_id, dosen_id) VALUES (?,?,?)",
        pengampu_data,
    )
    _ = cursor.executemany(
        "INSERT OR IGNORE INTO preferensi_dosen (id, dosen_id, waktu_id, hindari) VALUES (?,?,?,?)",
        preferensi_data,
    )

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' siap digunakan.")


def load_data_from_db(db_name: str = DB_FILE):
    """
    Memuat semua data dari database dan mengisinya ke dalam variabel global.
    """
    global ruangans, dosens, waktus, mata_kuliahs, pengampus, preferensi_dosens
    global \
        ruangan_map, \
        dosen_map, \
        waktu_map, \
        mata_kuliah_map, \
        pengampu_map, \
        preferensi_set
    global ruangan_teori_ids, ruangan_praktek_ids, waktu_ids

    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # Memudahkan akses kolom berdasarkan nama
    cursor = conn.cursor()

    # Load Ruangan
    _ = cursor.execute("SELECT * FROM ruangan")
    ruangans = [Ruangan(**row) for row in cursor.fetchall()]
    ruangan_map = {r.id: r for r in ruangans}
    ruangan_teori_ids = [r.id for r in ruangans if r.jenis == "teori"]
    ruangan_praktek_ids = [r.id for r in ruangans if r.jenis == "praktek"]

    # Load Dosen
    _ = cursor.execute("SELECT * FROM dosen")
    dosens = [Dosen(**row) for row in cursor.fetchall()]
    dosen_map = {d.id: d for d in dosens}

    # Load Waktu
    _ = cursor.execute("SELECT * FROM waktu")
    waktus = [Waktu(**row) for row in cursor.fetchall()]
    waktu_map = {w.id: w for w in waktus}
    waktu_ids = [w.id for w in waktus]

    # Load Mata Kuliah
    _ = cursor.execute("SELECT * FROM mata_kuliah")
    mata_kuliahs = [MataKuliah(**row) for row in cursor.fetchall()]
    mata_kuliah_map = {mk.id: mk for mk in mata_kuliahs}

    # Load Pengampu
    _ = cursor.execute("SELECT mata_kuliah_id, dosen_id FROM pengampu")
    pengampus = [Pengampu(**row) for row in cursor.fetchall()]
    pengampu_map = {p.mata_kuliah_id: p.dosen_id for p in pengampus}

    # Load Preferensi Dosen
    _ = cursor.execute(
        "SELECT dosen_id, waktu_id, hindari FROM preferensi_dosen WHERE hindari = 1"
    )
    preferensi_dosens = [PreferensiDosen(**row) for row in cursor.fetchall()]
    preferensi_set = {(p.dosen_id, p.waktu_id) for p in preferensi_dosens}

    conn.close()
    print("Semua data berhasil dimuat dari database.")
