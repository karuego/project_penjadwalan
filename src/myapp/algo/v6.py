import random
import math
import copy
import sqlite3
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple

# --- 1. DEFINISI STRTUR DATA (Model Final) ---

@dataclass
class Ruangan:
    id: int
    nama: str
    jenis: str

@dataclass
class Pengajar:
    id: int
    nama: str
    tipe: str

@dataclass
class MataKuliah:
    id: int
    nama: str
    semester: int

@dataclass
class KomponenMK:
    id: int
    mata_kuliah_id: int
    nama_komponen: str
    durasi_blok: int
    jenis: str
    jumlah_kelas: int
    jumlah_sesi_praktikum: int
    semester: int

@dataclass
class Waktu:
    id: int
    hari: str
    jam_mulai: str
    jam_selesai: str

@dataclass
class JadwalItem:
    """Unit terkecil yang dijadwalkan, sekarang dengan sesi dan status online."""
    unique_id: int
    komponen_mk_id: int
    kelas: str
    sesi_ke: int
    pengajar_id: int
    waktu_id_start: int
    ruangan_id: int or None
    daring: bool
    semester: int
    durasi_blok: int
    jenis: str

# --- Variabel Global ---
ruangans: List[Ruangan] = []
pengajars: List[Pengajar] = []
waktus: List[Waktu] = []
komponen_mks: List[KomponenMK] = []
ruangan_map: Dict[int, Ruangan] = {}
pengajar_map: Dict[int, Pengajar] = {}
waktu_map: Dict[int, Waktu] = {}
komponen_mk_map: Dict[int, KomponenMK] = {}
pengampu_map: Dict[int, int] = {}
waktu_start_options: Dict[int, List[int]] = {}
# Fitur Baru: Set untuk menyimpan preferensi yang dihindari
preferensi_hindari_set: Set[Tuple[int, int]] = set()


# --- 2. FUNGSI DATABASE (Struktur Diperbarui) ---

def setup_database(db_name="jadwal_advanced.db"):
    """Membuat DB dengan skema baru yang mendukung preferensi pengajar."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    tables = ['jadwal', 'preferensi_pengajar', 'pengampu', 'waktu', 'komponen_mk', 'mata_kuliah', 'pengajar', 'ruangan']
    for table in tables: cursor.execute(f"DROP TABLE IF EXISTS {table};")

    cursor.executescript("""
        CREATE TABLE ruangan (id INTEGER PRIMARY KEY, nama TEXT UNIQUE NOT NULL, jenis TEXT NOT NULL);
        CREATE TABLE pengajar (id INTEGER PRIMARY KEY, nama TEXT NOT NULL, tipe TEXT NOT NULL);
        CREATE TABLE mata_kuliah (id INTEGER PRIMARY KEY, nama TEXT NOT NULL, semester INTEGER NOT NULL);
        CREATE TABLE komponen_mk (
            id INTEGER PRIMARY KEY,
            mata_kuliah_id INTEGER NOT NULL,
            nama_komponen TEXT NOT NULL,
            durasi_blok INTEGER NOT NULL,
            jenis TEXT NOT NULL,
            jumlah_kelas INTEGER NOT NULL,
            jumlah_sesi_praktikum INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (mata_kuliah_id) REFERENCES mata_kuliah(id)
        );
        CREATE TABLE waktu (id INTEGER PRIMARY KEY, hari TEXT NOT NULL, jam_mulai TEXT NOT NULL, jam_selesai TEXT NOT NULL);
        CREATE TABLE pengampu (id INTEGER PRIMARY KEY, komponen_mk_id INTEGER NOT NULL, pengajar_id INTEGER NOT NULL, FOREIGN KEY (komponen_mk_id) REFERENCES komponen_mk(id), FOREIGN KEY (pengajar_id) REFERENCES pengajar(id));

        /* -- Tabel Baru untuk Preferensi -- */
        CREATE TABLE preferensi_pengajar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pengajar_id INTEGER NOT NULL,
            waktu_id INTEGER NOT NULL,
            FOREIGN KEY (pengajar_id) REFERENCES pengajar(id),
            FOREIGN KEY (waktu_id) REFERENCES waktu(id)
        );

        CREATE TABLE jadwal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            komponen_mk_id INTEGER NOT NULL,
            kelas CHAR NOT NULL,
            sesi_ke INTEGER NOT NULL,
            ruangan_id INTEGER,
            pengajar_id INTEGER NOT NULL,
            waktu_id_start INTEGER NOT NULL,
            durasi_blok INTEGER NOT NULL,
            daring BOOLEAN NOT NULL DEFAULT FALSE,
            FOREIGN KEY (komponen_mk_id) REFERENCES komponen_mk(id)
        );
    """)

    # Data Sampel Baru
    ruangan_data = [(1, 'R-Teori-A', 'teori'), (2, 'Lab-Komputer-1', 'praktek')]
    pengajar_data = [(1, 'Dr. Budi', 'Dosen'), (2, 'Dr. Ani', 'Dosen'), (101, 'Asisten Lab A', 'Asisten')]
    mata_kuliah_data = [(1, 'Basis Data', 3), (2, 'Algoritma', 1), (3, 'Jaringan Komputer', 3)]
    komponen_mk_data = [
        (1, 1, 'Teori Basis Data', 2, 'teori', 1, 1),
        (2, 1, 'Praktikum Basis Data', 1, 'praktek', 1, 2),
        (3, 2, 'Teori Algoritma', 2, 'teori', 1, 1),
        (4, 2, 'Praktikum Algoritma', 2, 'praktek', 1, 1),
        (5, 3, 'Teori Jaringan Komputer', 2, 'teori', 1, 1)
    ]
    pengampu_data = [(1, 1, 1), (2, 2, 101), (3, 3, 2), (4, 4, 101), (5, 5, 1)]

    # Data Sampel Preferensi: Dr. Budi (id=1) ingin menghindari 2 jam pertama di hari Senin (waktu_id=1 dan 2)
    preferensi_data = [(1, 1), (1, 2)]

    waktu_data = []
    waktu_id = 1
    for hari in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']:
        waktu = [8, 0]

        while waktu[0] < 17:
            jam = waktu[0]
            menit = waktu[1]

            waktu_mulai = jam * 60 + menit
            waktu_selesai = waktu_mulai + 45

            start_h, start_m = divmod(waktu_mulai, 60)
            end_h, end_m = divmod(waktu_selesai, 60)

            waktu[0] = end_h
            waktu[1] = end_m

            if jam == 12: continue

            data = (waktu_id, hari, f"{start_h:02d}:{start_m:02d}", f"{end_h:02d}:{end_m:02d}")
            waktu_data.append(data)
            waktu_id += 1

    cursor.executemany("INSERT INTO ruangan VALUES (?,?,?)", ruangan_data)
    cursor.executemany("INSERT INTO pengajar VALUES (?,?,?)", pengajar_data)
    cursor.executemany("INSERT INTO mata_kuliah VALUES (?,?,?)", mata_kuliah_data)
    cursor.executemany("INSERT INTO komponen_mk VALUES (?,?,?,?,?,?,?)", komponen_mk_data)
    cursor.executemany("INSERT INTO waktu VALUES (?,?,?,?)", waktu_data)
    cursor.executemany("INSERT INTO pengampu VALUES (?,?,?)", pengampu_data)
    cursor.executemany("INSERT INTO preferensi_pengajar (pengajar_id, waktu_id) VALUES (?,?)", preferensi_data)

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' dengan fitur preferensi siap digunakan.")

def load_data_from_db(db_name="jadwal_advanced.db"):
    """Memuat semua data dari DB, termasuk preferensi pengajar."""
    global ruangans, pengajars, waktus, komponen_mks, ruangan_map, pengajar_map, waktu_map, komponen_mk_map, pengampu_map, waktu_start_options, preferensi_hindari_set
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    ruangans = [Ruangan(**row) for row in cursor.execute("SELECT * FROM ruangan").fetchall()]
    ruangan_map = {r.id: r for r in ruangans}
    pengajars = [Pengajar(**row) for row in cursor.execute("SELECT * FROM pengajar").fetchall()]
    pengajar_map = {p.id: p for p in pengajars}
    waktus = [Waktu(**row) for row in cursor.execute("SELECT * FROM waktu ORDER BY id").fetchall()]
    waktu_map = {w.id: w for w in waktus}
    query_komponen = "SELECT k.*, mk.semester FROM komponen_mk k JOIN mata_kuliah mk ON k.mata_kuliah_id = mk.id"
    komponen_mks = [KomponenMK(**row) for row in cursor.execute(query_komponen).fetchall()]
    komponen_mk_map = {k.id: k for k in komponen_mks}
    pengampu_map = {row['komponen_mk_id']: row['pengajar_id'] for row in cursor.execute("SELECT * FROM pengampu").fetchall()}

    # Memuat data preferensi
    preferensi_hindari_set = {(row['pengajar_id'], row['waktu_id']) for row in cursor.execute("SELECT * FROM preferensi_pengajar").fetchall()}

    max_durasi = max(k.durasi_blok for k in komponen_mks) if komponen_mks else 1
    waktu_by_hari = {h: [w.id for w in sorted(waktus, key=lambda x: x.id) if w.hari == h] for h in set(w.hari for w in waktus)}
    for durasi in range(1, max_durasi + 1):
        waktu_start_options[durasi] = []
        for hari in waktu_by_hari:
            blok_harian = waktu_by_hari[hari]
            for i in range(len(blok_harian) - durasi + 1):
                if blok_harian[i+durasi-1] == blok_harian[i] + durasi - 1:
                    waktu_start_options[durasi].append(blok_harian[i])
    conn.close()
    print("Semua data berhasil dimuat dari database.")

def save_schedule_to_db(schedule: List[JadwalItem], db_name="jadwal_advanced.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jadwal;")
    schedule_data = [(item.komponen_mk_id, item.kelas, item.sesi_ke, item.ruangan_id, item.pengajar_id, item.waktu_id_start, item.durasi_blok, item.daring) for item in schedule]
    cursor.executemany("INSERT INTO jadwal (komponen_mk_id, kelas, sesi_ke, ruangan_id, pengajar_id, waktu_id_start, durasi_blok, daring) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", schedule_data)
    conn.commit()
    conn.close()
    print(f"\nJadwal optimal telah disimpan ke database '{db_name}'.")

# --- 3. LOGIKA ALGORITMA (Diperbarui) ---

def generate_initial_solution() -> List[JadwalItem]:
    """Membuat jadwal awal, kini menghandle sesi praktikum dan kelas online."""
    initial_schedule = []
    ruangan_teori_ids = [r.id for r in ruangans if r.jenis == 'teori']
    ruangan_praktek_ids = [r.id for r in ruangans if r.jenis == 'praktek']
    unique_id_counter = 0

    for komp in komponen_mks:
        for i in range(komp.jumlah_kelas):
            kelas_char = chr(ord('A') + i)
            num_sessions = komp.jumlah_sesi_praktikum if komp.jenis == 'praktek' else 1
            for sesi in range(1, num_sessions + 1):
                start_time_id = random.choice(waktu_start_options[komp.durasi_blok])
                is_daring = False
                ruangan_id = None
                if komp.jenis == 'teori':
                    if random.random() < 0.1 and ruangan_teori_ids:
                        is_daring = True
                    else:
                        ruangan_id = random.choice(ruangan_teori_ids) if ruangan_teori_ids else None
                        if not ruangan_id: is_daring = True
                else:
                    ruangan_id = random.choice(ruangan_praktek_ids) if ruangan_praktek_ids else None
                initial_schedule.append(JadwalItem(
                    unique_id=unique_id_counter, komponen_mk_id=komp.id, kelas=kelas_char, sesi_ke=sesi,
                    pengajar_id=pengampu_map[komp.id], waktu_id_start=start_time_id,
                    ruangan_id=ruangan_id, daring=is_daring, semester=komp.semester,
                    durasi_blok=komp.durasi_blok, jenis=komp.jenis
                ))
                unique_id_counter += 1
    return initial_schedule

def calculate_cost(schedule: List[JadwalItem]) -> int:
    """Menghitung biaya, dengan logika bentrok mahasiswa yang telah diperbaiki."""
    cost = 0
    PENALTI_BENTROK = 100
    PENALTI_DARING = 5
    PENALTI_PREFERENSI = 1

    ruangan_waktu_check = set()
    pengajar_waktu_check = set()
    # Logika baru untuk bentrok mahasiswa yang lebih akurat
    mahasiswa_waktu_check: Dict[int, Set[Tuple]] = {}

    for item in schedule:
        if item.daring:
            cost += PENALTI_DARING

        waktu_blok_ids = range(item.waktu_id_start, item.waktu_id_start + item.durasi_blok)

        # --- Logika Bentrok Mahasiswa Baru ---
        is_split = item.jenis == 'praktek' and komponen_mk_map[item.komponen_mk_id].jumlah_sesi_praktikum > 1

        current_item_groups_to_add = set()
        if is_split:
            # Sesi praktikum yang dipecah hanya membuat grup sesinya sibuk
            current_item_groups_to_add.add(('session', item.semester, item.kelas, item.sesi_ke))
        else:
            # Teori atau praktikum biasa membuat seluruh kelas sibuk
            current_item_groups_to_add.add(('whole_class', item.semester, item.kelas))
        # --- End of setup ---

        for blok_id in waktu_blok_ids:
            # Cek Pelanggaran Preferensi
            if (item.pengajar_id, blok_id) in preferensi_hindari_set:
                cost += PENALTI_PREFERENSI

            # Cek Bentrok Ruangan & Pengajar (Logika Lama)
            if not item.daring and item.ruangan_id is not None:
                if (item.ruangan_id, blok_id) in ruangan_waktu_check: cost += PENALTI_BENTROK
                ruangan_waktu_check.add((item.ruangan_id, blok_id))
            if (item.pengajar_id, blok_id) in pengajar_waktu_check: cost += PENALTI_BENTROK
            pengajar_waktu_check.add((item.pengajar_id, blok_id))

            # --- Cek Bentrok Mahasiswa (Logika Baru) ---
            if blok_id not in mahasiswa_waktu_check:
                mahasiswa_waktu_check[blok_id] = set()

            busy_groups_in_block = mahasiswa_waktu_check[blok_id]
            is_clash = False

            # 1. Apakah seluruh kelas sudah sibuk oleh jadwal lain?
            if ('whole_class', item.semester, item.kelas) in busy_groups_in_block:
                is_clash = True

            # 2. Jika jadwal ini untuk seluruh kelas, apakah ada sesi praktikum yang sedang berjalan?
            if not is_split:
                for group in busy_groups_in_block:
                    if group[0] == 'session' and group[1] == item.semester and group[2] == item.kelas:
                        is_clash = True
                        break

            # 3. Jika ini sesi praktikum, apakah sesi yang sama persis sudah ada? (mencegah duplikat)
            if is_split and ('session', item.semester, item.kelas, item.sesi_ke) in busy_groups_in_block:
                 is_clash = True

            if is_clash:
                cost += PENALTI_BENTROK

            # Update setelah cek selesai untuk blok ini
            mahasiswa_waktu_check[blok_id].update(current_item_groups_to_add)

    return cost

def get_neighbor_solution(schedule: List[JadwalItem]) -> List[JadwalItem]:
    """Membuat solusi tetangga, kini bisa mengubah status online."""
    neighbor = copy.deepcopy(schedule)
    if not neighbor: return neighbor

    item_to_change = random.choice(neighbor)

    ruangan_teori_ids = [r.id for r in ruangans if r.jenis == 'teori']
    ruangan_praktek_ids = [r.id for r in ruangans if r.jenis == 'praktek']

    move_type = random.random()
    if move_type < 0.6:
        item_to_change.waktu_id_start = random.choice(waktu_start_options[item_to_change.durasi_blok])
    elif move_type < 0.8 and not item_to_change.daring:
        if item_to_change.jenis == 'teori' and ruangan_teori_ids:
            item_to_change.ruangan_id = random.choice(ruangan_teori_ids)
        elif item_to_change.jenis == 'praktek' and ruangan_praktek_ids:
            item_to_change.ruangan_id = random.choice(ruangan_praktek_ids)
    elif item_to_change.jenis == 'teori' and ruangan_teori_ids:
        if item_to_change.daring:
            item_to_change.daring = False
            item_to_change.ruangan_id = random.choice(ruangan_teori_ids)
        else:
            item_to_change.daring = True
            item_to_change.ruangan_id = None

    return neighbor

def simulated_annealing(max_iterations=300000):
    print("\nMemulai proses optimasi (dengan preferensi, sesi & online)...")
    temp = 1000.0
    cooling_rate = 0.99995

    current_solution = generate_initial_solution()
    current_cost = calculate_cost(current_solution)
    best_solution, best_cost = copy.deepcopy(current_solution), current_cost

    print(f"Biaya Awal: {best_cost}")

    for i in range(max_iterations):
        if temp <= 0.1: break
        neighbor = get_neighbor_solution(current_solution)
        neighbor_cost = calculate_cost(neighbor)
        cost_diff = neighbor_cost - current_cost
        if cost_diff < 0 or random.random() < math.exp(-cost_diff / temp):
            current_solution, current_cost = neighbor, neighbor_cost
        if current_cost < best_cost:
            best_solution, best_cost = copy.deepcopy(current_solution), current_cost
            print(f"Iterasi {i}: Solusi lebih baik -> Biaya {best_cost}")
            if best_cost == 0:
                print("Solusi optimal (tanpa bentrok & semua preferensi terpenuhi) ditemukan!")
                break
        temp *= cooling_rate

    print("\nProses optimasi selesai.")
    return best_solution, best_cost

# --- 4. FUNGSI TAMPILAN ---

def print_schedule(schedule: List[JadwalItem], cost: int):
    print("\n" + "="*45 + "\n           HASIL PENJADWALAN OPTIMAL\n" + "="*45)
    print(f"Total Biaya (Penalti): {cost}")

    # Memecah biaya untuk laporan yang lebih detail
    bentrok = cost // 100
    sisa_biaya = cost % 100
    online = sisa_biaya // 5
    preferensi = sisa_biaya % 5

    print(f"Status: {bentrok} bentrok, {online} kelas online, {preferensi} preferensi terlanggar.")
    print("-" * 45 + "\n")

    schedule.sort(key=lambda x: (waktu_map[x.waktu_id_start].hari, x.waktu_id_start))

    hari_sekarang = ""
    for item in schedule:
        w_start = waktu_map[item.waktu_id_start]
        if w_start.hari != hari_sekarang:
            hari_sekarang = w_start.hari
            print(f"--- HARI: {hari_sekarang.upper()} ---")

        komp = komponen_mk_map[item.komponen_mk_id]
        pengajar = pengajar_map[item.pengajar_id]
        w_end = waktu_map[item.waktu_id_start + item.durasi_blok - 1]

        lokasi = ""
        if item.daring:
            lokasi = "(Online)"
        elif item.ruangan_id:
            lokasi = ruangan_map[item.ruangan_id].nama
        else:
            lokasi = "(RUANG TIDAK DITEMUKAN)"

        sesi_info = f" (Sesi {item.sesi_ke})" if komp.jumlah_sesi_praktikum > 1 else ""

        print(f"[{w_start.jam_mulai}-{w_end.jam_selesai}] {komp.nama_komponen}{sesi_info} - Kelas {item.kelas} (Sem {item.semester})\n"
              f"  -> Pengajar: {pengajar.nama} ({pengajar.tipe})\n"
              f"  -> Lokasi  : {lokasi}\n")

# --- 5. EKSEKUSI PROGRAM ---
if __name__ == "__main__":
    DB_FILE = "jadwal_advanced_v6.db"
    setup_database(DB_FILE)
    load_data_from_db(DB_FILE)

    final_schedule, final_cost = simulated_annealing()

    print_schedule(final_schedule, final_cost)
    if final_schedule:
        save_schedule_to_db(final_schedule, DB_FILE)
