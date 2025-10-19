import random
import math
import copy
import sqlite3
from dataclasses import dataclass, field
from typing import List, Dict, Set

# --- 1. DEFINISI STRUKTUR DATA (Berdasarkan DBML) ---
# Struktur ini tetap sama, digunakan untuk menampung data dari database.

@dataclass
class Ruangan:
    id: int
    nama: str
    jenis: str # 'teori' atau 'praktek'

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
    jenis: str # 'teori' atau 'praktek'

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
    kelas: str # 'A', 'B', dst.
    dosen_id: int
    waktu_id: int
    ruangan_id: int
    semester: int
    jenis_mk: str # 'teori' atau 'praktek'

# --- Variabel Global untuk menyimpan data yang dimuat ---
# Variabel ini akan diisi oleh fungsi `load_data_from_db`
ruangans: List[Ruangan] = []
dosens: List[Dosen] = []
waktus: List[Waktu] = []
mata_kuliahs: List[MataKuliah] = []
pengampus: List[Pengampu] = []
preferensi_dosens: List[PreferensiDosen] = []

# Helper Maps and Sets
ruangan_map: Dict[int, Ruangan] = {}
dosen_map: Dict[int, Dosen] = {}
waktu_map: Dict[int, Waktu] = {}
mata_kuliah_map: Dict[int, MataKuliah] = {}
pengampu_map: Dict[int, int] = {}
preferensi_set: Set = set()
ruangan_teori_ids: List[int] = []
ruangan_praktek_ids: List[int] = []
waktu_ids: List[int] = []


# --- 2. FUNGSI DATABASE ---

def setup_database(db_name="jadwal.db"):
    """
    Membuat dan mengisi database SQLite dengan data awal jika belum ada.
    Fungsi ini bersifat idempoten, aman untuk dijalankan berkali-kali.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Membuat Tabel
    cursor.executescript("""
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
        -- Tabel untuk menyimpan hasil akhir
        CREATE TABLE IF NOT EXISTS jadwal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mata_kuliah_id INTEGER NOT NULL,
            kelas CHAR NOT NULL,
            ruangan_id INTEGER NOT NULL,
            dosen_id INTEGER NOT NULL,
            waktu_id INTEGER NOT NULL,
            FOREIGN KEY (mata_kuliah_id) REFERENCES mata_kuliah(id),
            FOREIGN KEY (ruangan_id) REFERENCES ruangan(id),
            FOREIGN KEY (dosen_id) REFERENCES dosen(id),
            FOREIGN KEY (waktu_id) REFERENCES waktu(id)
        );
    """)

    # Kosongkan tabel hasil setiap kali dijalankan
    cursor.execute("DELETE FROM jadwal;")

    # Data Sampel untuk dimasukkan ke DB
    ruangan_data = [(1, 'R-101', 'teori'), (2, 'R-102', 'teori'), (3, 'Lab-Kom A', 'praktek'), (4, 'Lab-Kom B', 'praktek')]
    dosen_data = [(1, 'Dr. Budi'), (2, 'Dr. Ani'), (3, 'Dr. Candra')]
    waktu_data = [
        (1, 'Senin', '08:00', '10:00'), (2, 'Senin', '10:00', '12:00'),
        (3, 'Senin', '13:00', '15:00'), (4, 'Senin', '15:00', '17:00'),
        (5, 'Selasa', '08:00', '10:00'), (6, 'Selasa', '10:00', '12:00'),
        (7, 'Selasa', '13:00', '15:00'), (8, 'Selasa', '15:00', '17:00')
    ]
    mata_kuliah_data = [
        (1, 'Basis Data', 3, 2, 'teori'), (2, 'Praktikum Basis Data', 3, 2, 'praktek'),
        (3, 'Kecerdasan Buatan', 5, 1, 'teori'), (4, 'Jaringan Komputer', 5, 1, 'teori')
    ]
    pengampu_data = [(1, 1, 1), (2, 2, 1), (3, 3, 2), (4, 4, 3)]
    preferensi_data = [(1, 2, 1, 1), (2, 3, 8, 1)]

    # Mengisi data menggunakan INSERT OR IGNORE agar tidak error jika data sudah ada
    cursor.executemany("INSERT OR IGNORE INTO ruangan (id, nama, jenis) VALUES (?,?,?)", ruangan_data)
    cursor.executemany("INSERT OR IGNORE INTO dosen (id, nama) VALUES (?,?)", dosen_data)
    cursor.executemany("INSERT OR IGNORE INTO waktu (id, hari, jam_mulai, jam_selesai) VALUES (?,?,?,?)", waktu_data)
    cursor.executemany("INSERT OR IGNORE INTO mata_kuliah (id, nama, semester, jumlah_kelas, jenis) VALUES (?,?,?,?,?)", mata_kuliah_data)
    cursor.executemany("INSERT OR IGNORE INTO pengampu (id, mata_kuliah_id, dosen_id) VALUES (?,?,?)", pengampu_data)
    cursor.executemany("INSERT OR IGNORE INTO preferensi_dosen (id, dosen_id, waktu_id, hindari) VALUES (?,?,?,?)", preferensi_data)

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' siap digunakan.")

def load_data_from_db(db_name="jadwal.db"):
    """
    Memuat semua data dari database dan mengisinya ke dalam variabel global.
    """
    global ruangans, dosens, waktus, mata_kuliahs, pengampus, preferensi_dosens
    global ruangan_map, dosen_map, waktu_map, mata_kuliah_map, pengampu_map, preferensi_set
    global ruangan_teori_ids, ruangan_praktek_ids, waktu_ids

    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row # Memudahkan akses kolom berdasarkan nama
    cursor = conn.cursor()

    # Load Ruangan
    cursor.execute("SELECT * FROM ruangan")
    ruangans = [Ruangan(**row) for row in cursor.fetchall()]
    ruangan_map = {r.id: r for r in ruangans}
    ruangan_teori_ids = [r.id for r in ruangans if r.jenis == 'teori']
    ruangan_praktek_ids = [r.id for r in ruangans if r.jenis == 'praktek']

    # Load Dosen
    cursor.execute("SELECT * FROM dosen")
    dosens = [Dosen(**row) for row in cursor.fetchall()]
    dosen_map = {d.id: d for d in dosens}

    # Load Waktu
    cursor.execute("SELECT * FROM waktu")
    waktus = [Waktu(**row) for row in cursor.fetchall()]
    waktu_map = {w.id: w for w in waktus}
    waktu_ids = [w.id for w in waktus]

    # Load Mata Kuliah
    cursor.execute("SELECT * FROM mata_kuliah")
    mata_kuliahs = [MataKuliah(**row) for row in cursor.fetchall()]
    mata_kuliah_map = {mk.id: mk for mk in mata_kuliahs}

    # Load Pengampu
    cursor.execute("SELECT mata_kuliah_id, dosen_id FROM pengampu")
    pengampus = [Pengampu(**row) for row in cursor.fetchall()]
    pengampu_map = {p.mata_kuliah_id: p.dosen_id for p in pengampus}

    # Load Preferensi Dosen
    cursor.execute("SELECT dosen_id, waktu_id, hindari FROM preferensi_dosen WHERE hindari = 1")
    preferensi_dosens = [PreferensiDosen(**row) for row in cursor.fetchall()]
    preferensi_set = {(p.dosen_id, p.waktu_id) for p in preferensi_dosens}

    conn.close()
    print("Semua data berhasil dimuat dari database.")

def save_schedule_to_db(schedule: List[JadwalItem], db_name="jadwal.db"):
    """
    Menyimpan jadwal hasil optimasi ke dalam tabel 'jadwal' di database.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Siapkan data untuk dimasukkan
    schedule_data = [
        (item.mata_kuliah_id, item.kelas, item.ruangan_id, item.dosen_id, item.waktu_id)
        for item in schedule
    ]

    # Masukkan semua data jadwal
    cursor.executemany(
        "INSERT INTO jadwal (mata_kuliah_id, kelas, ruangan_id, dosen_id, waktu_id) VALUES (?, ?, ?, ?, ?)",
        schedule_data
    )

    conn.commit()
    conn.close()
    print(f"\nJadwal optimal telah disimpan ke dalam tabel 'jadwal' di database '{db_name}'.")


# --- 3. FUNGSI UNTUK MEMBUAT JADWAL AWAL ---
# Fungsi ini tidak perlu diubah karena sudah menggunakan variabel global yang diisi dari DB
def generate_initial_solution() -> List[JadwalItem]:
    initial_schedule = []
    list_kelas_untuk_dijadwalkan = []
    for mk in mata_kuliahs:
        for i in range(mk.jumlah_kelas):
            kelas_char = chr(ord('A') + i)
            list_kelas_untuk_dijadwalkan.append({
                'mata_kuliah_id': mk.id,
                'kelas': kelas_char,
                'semester': mk.semester,
                'jenis_mk': mk.jenis,
                'dosen_id': pengampu_map[mk.id]
            })

    for kelas_info in list_kelas_untuk_dijadwalkan:
        waktu_terpilih = random.choice(waktu_ids)
        if kelas_info['jenis_mk'] == 'teori':
            ruangan_terpilih = random.choice(ruangan_teori_ids)
        else:
            ruangan_terpilih = random.choice(ruangan_praktek_ids)

        jadwal_item = JadwalItem(
            mata_kuliah_id=kelas_info['mata_kuliah_id'],
            kelas=kelas_info['kelas'],
            dosen_id=kelas_info['dosen_id'],
            waktu_id=waktu_terpilih,
            ruangan_id=ruangan_terpilih,
            semester=kelas_info['semester'],
            jenis_mk=kelas_info['jenis_mk']
        )
        initial_schedule.append(jadwal_item)
    return initial_schedule

# --- 4. FUNGSI BIAYA (COST FUNCTION) ---
# Tidak ada perubahan
def calculate_cost(schedule: List[JadwalItem]) -> int:
    cost = 0
    PENALTI_HARD = 100
    PENALTI_SOFT = 1
    ruangan_waktu_check = set()
    dosen_waktu_check = set()
    mahasiswa_waktu_check = set()
    for item in schedule:
        if (item.ruangan_id, item.waktu_id) in ruangan_waktu_check:
            cost += PENALTI_HARD
        else:
            ruangan_waktu_check.add((item.ruangan_id, item.waktu_id))
        if (item.dosen_id, item.waktu_id) in dosen_waktu_check:
            cost += PENALTI_HARD
        else:
            dosen_waktu_check.add((item.dosen_id, item.waktu_id))
        if (item.semester, item.waktu_id) in mahasiswa_waktu_check:
            cost += PENALTI_HARD
        else:
            mahasiswa_waktu_check.add((item.semester, item.waktu_id))
    for item in schedule:
        if (item.dosen_id, item.waktu_id) in preferensi_set:
            cost += PENALTI_SOFT
    return cost

# --- 5. FUNGSI UNTUK MENDAPATKAN SOLUSI TETANGGA ---
# Tidak ada perubahan
def get_neighbor_solution(schedule: List[JadwalItem]) -> List[JadwalItem]:
    neighbor = copy.deepcopy(schedule)
    if not neighbor:
        return neighbor
    item_to_change_idx = random.randrange(len(neighbor))
    item_to_change = neighbor[item_to_change_idx]
    if random.random() < 0.5:
        new_waktu_id = random.choice(waktu_ids)
        item_to_change.waktu_id = new_waktu_id
    else:
        if item_to_change.jenis_mk == 'teori':
            new_ruangan_id = random.choice(ruangan_teori_ids)
        else:
            new_ruangan_id = random.choice(ruangan_praktek_ids)
        item_to_change.ruangan_id = new_ruangan_id
    return neighbor

# --- 6. ALGORITMA SIMULATED ANNEALING ---
# Tidak ada perubahan
def simulated_annealing(initial_temp: float, cooling_rate: float, stopping_temp: float, max_iterations: int):
    print("\nMemulai proses optimasi dengan Simulated Annealing...")
    current_solution = generate_initial_solution()
    current_cost = calculate_cost(current_solution)
    best_solution = copy.deepcopy(current_solution)
    best_cost = current_cost
    temperature = initial_temp
    iteration = 0
    print(f"Biaya Awal: {current_cost}")
    while temperature > stopping_temp and iteration < max_iterations:
        neighbor_solution = get_neighbor_solution(current_solution)
        neighbor_cost = calculate_cost(neighbor_solution)
        cost_difference = neighbor_cost - current_cost
        if cost_difference < 0:
            current_solution = neighbor_solution
            current_cost = neighbor_cost
        else:
            acceptance_probability = math.exp(-cost_difference / temperature)
            if random.random() < acceptance_probability:
                current_solution = neighbor_solution
                current_cost = neighbor_cost
        if current_cost < best_cost:
            best_solution = copy.deepcopy(current_solution)
            best_cost = current_cost
            if best_cost == 0:
                print(f"Iterasi {iteration}: Solusi optimal ditemukan! Biaya -> {best_cost}")
                break
            else:
                print(f"Iterasi {iteration}: Ditemukan solusi lebih baik dengan biaya -> {best_cost}")
        temperature *= cooling_rate
        iteration += 1
        if iteration % 2000 == 0:
            print(f"Iterasi {iteration}, Suhu: {temperature:.2f}, Biaya Saat Ini: {current_cost}, Biaya Terbaik: {best_cost}")
    print("\nProses optimasi selesai.")
    return best_solution, best_cost

# --- 7. FUNGSI UNTUK MENAMPILKAN HASIL ---
# Tidak ada perubahan
def print_schedule(schedule: List[JadwalItem], cost: int):
    print("\n======================================")
    print("      HASIL PENJADWALAN OPTIMAL     ")
    print("======================================")
    print(f"Total Biaya (Penalti): {cost}")
    if cost == 0:
        print("Status: Optimal (Tidak ada konflik ditemukan)")
    else:
        print(f"Status: Sub-optimal (Masih ada {cost // 100} konflik & {cost % 100} pelanggaran preferensi)")
    print("--------------------------------------\n")
    schedule_by_day = {w.hari: [] for w in waktus}
    for item in schedule:
        hari = waktu_map[item.waktu_id].hari
        schedule_by_day[hari].append(item)
    for hari, items in sorted(schedule_by_day.items()):
        if not items: continue
        print(f"--- HARI: {hari.upper()} ---")
        sorted_items = sorted(items, key=lambda x: waktu_map[x.waktu_id].jam_mulai)
        for item in sorted_items:
            mk = mata_kuliah_map[item.mata_kuliah_id]
            dosen = dosen_map[item.dosen_id]
            waktu = waktu_map[item.waktu_id]
            ruangan = ruangan_map[item.ruangan_id]
            print(
                f"[{waktu.jam_mulai}-{waktu.jam_selesai}] {mk.nama} (Kelas {item.kelas}) - Sem {item.semester}\n"
                f"  -> Dosen  : {dosen.nama}\n"
                f"  -> Ruangan: {ruangan.nama} ({ruangan.jenis})\n"
            )
        print()

# --- 8. EKSEKUSI PROGRAM ---
if __name__ == "__main__":
    DB_FILE = "jadwal.db"
    
    # 1. Siapkan database (buat dan isi jika perlu)
    # setup_database(DB_FILE)
    
    # 2. Muat data dari database ke dalam program
    load_data_from_db(DB_FILE)

    # 3. Jalankan algoritma dengan data yang sudah dimuat
    INITIAL_TEMPERATURE = 1000.0
    COOLING_RATE = 0.995
    STOPPING_TEMPERATURE = 0.1
    MAX_ITERATIONS = 50000
    
    final_schedule, final_cost = simulated_annealing(
        INITIAL_TEMPERATURE,
        COOLING_RATE,
        STOPPING_TEMPERATURE,
        MAX_ITERATIONS
    )
    
    # 4. Tampilkan hasil
    print_schedule(final_schedule, final_cost)
    
    # 5. Simpan hasil ke database
    if final_schedule:
        save_schedule_to_db(final_schedule, DB_FILE)
