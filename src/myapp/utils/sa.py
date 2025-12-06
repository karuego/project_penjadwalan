from myapp.utils.struct_ruangan import Ruangan
from myapp.utils.schedule_item import ScheduleItem
import random
import math
import copy
import sqlite3
import re
from typing import Callable
from dataclasses import replace

# --- IMPORT STRUCT ---
# Pastikan file-file struct berada dalam satu folder atau package yang bisa diakses
try:
    from myapp.utils.struct_ruangan import Ruangan
    from myapp.utils.struct_pengajar import Pengajar
    from myapp.utils.struct_matakuliah import MataKuliah
    from myapp.utils.struct_waktu import TimeSlot
    from myapp.utils.struct_jadwal import Jadwal
    from myapp.utils.hari import Hari
    from myapp.utils.database import Database

    from myapp.utils.schedule_item import ScheduleItem
except ImportError as e:
    print(f"Error importing structs: {e}")
    print("Pastikan file struct_*.py dan hari.py ada di direktori yang sama.")
    exit(1)


# --- VARIABEL GLOBAL ---
global_ruangans: list[Ruangan] = []
global_pengajars: list[Pengajar] = []
global_mks: list[MataKuliah] = []
global_timeslots: list[TimeSlot] = []

# Mappings untuk akses cepat (O(1))
ruangan_map: dict[int, Ruangan] = {}
pengajar_map: dict[str, Pengajar] = {}
mk_map: dict[int, MataKuliah] = {}

# Time Management
# List flat semua timeslot yang terurut berdasarkan (Hari, Jam Mulai)
sorted_timeslots: list[TimeSlot] = []
# Mapping: durasi (sks) -> list of valid start indices di sorted_timeslots
valid_start_indices: dict[int, list[int]] = {}

# DB_NAME = "jadwal_sa.db"  # Sesuaikan dengan nama file DB fisik Anda
DB_NAME = "database.sqlite3.db"  # Sesuaikan dengan nama file DB fisik Anda

# --- 2. FUNGSI DATABASE & INITIALIZATION ---


def get_db_connection():
    # return sqlite3.connect(DB_NAME)
    return Database().get_connection()


def load_data():
    """Memuat semua data dari database ke dalam Struct Objects."""
    global global_ruangans, global_pengajars, global_mks, global_timeslots
    global sorted_timeslots, valid_start_indices

    conn = get_db_connection()
    cursor = conn.cursor()

    print("Memuat data dari database...")

    # 1. Load Ruangan
    # Schema: id, nama, jenis
    _ = cursor.execute("SELECT id, nama, jenis FROM ruangan")
    res_ruangan: list[tuple[int, str, str]] = cursor.fetchall()
    global_ruangans = [
        Ruangan(id=row[0], nama=row[1], tipe=row[2]) for row in res_ruangan
    ]
    for r in global_ruangans:
        ruangan_map[r.getId()] = r

    # 2. Load Pengajar
    # Schema: id (text), nama, jenis, preferensi_waktu
    _ = cursor.execute("SELECT id, nama, jenis, preferensi_waktu FROM pengajar")
    res_pengajar: list[tuple[str, str, str, str]] = cursor.fetchall()
    global_pengajars = []
    for row in res_pengajar:
        # Handle potential NULL in preferensi_waktu
        pref: str = row[3] if row[3] else ""
        p = Pengajar(id=row[0], nama=row[1], tipe=row[2], waktu=pref)
        global_pengajars.append(p)
        pengajar_map[p.getId()] = p

    # 3. Load Mata Kuliah
    # Schema: id, nama, jenis, sks, semester, jumlah_kelas, pengajar_id
    _ = cursor.execute(
        "SELECT id, nama, jenis, sks, semester, jumlah_kelas, pengajar_id FROM mata_kuliah"
    )
    res: list[tuple[int, str, str, int, int, int, str]] = cursor.fetchall()
    global_mks = []
    for row in res:
        pengajar_id: str = row[6]
        pengajar_obj: Pengajar | None = pengajar_map.get(pengajar_id)

        if not pengajar_obj:
            print(
                f"Warning: Pengajar ID {pengajar_id} untuk MK {row[1]} tidak ditemukan."
            )
            continue

        mk = MataKuliah(
            id=row[0],
            nama=row[1],
            tipe=row[2],
            sks=row[3],
            semester=row[4],
            kelas=row[5],
            pengampu=pengajar_obj,
        )
        global_mks.append(mk)
        mk_map[mk.getId()] = mk  # pyright: ignore[reportArgumentType]

    # 4. Load TimeSlots
    # Schema: id, hari (int), mulai, selesai
    _ = cursor.execute(
        "SELECT id, hari, mulai, selesai FROM timeslots ORDER BY hari, mulai"
    )
    rows: list[tuple[int, int, str, str]] = cursor.fetchall()
    global_timeslots = [
        TimeSlot(id=row[0], hari=row[1], mulai=row[2], selesai=row[3]) for row in rows
    ]

    # Sort timeslots untuk memastikan urutan logis (Senin 07:00, Senin 08:00, dst)
    # Asumsi: hari berupa int (1=Senin, dst) dan mulai format "HH:MM" bisa disort string
    sorted_timeslots = sorted(
        global_timeslots, key=lambda x: (x.getHari(), x.getMulai())
    )

    # Pre-calculate valid start indices for continuous blocks
    # Logic: Jika MK butuh 3 SKS, kita butuh 3 slot berturut-turut di hari yang sama.
    max_sks = max((mk.getSks() for mk in global_mks), default=1)  # pyright: ignore[reportArgumentType]

    for duration in range(1, max_sks + 1):
        valid_indices: list[int] = []
        for i in range(len(sorted_timeslots) - duration + 1):
            # Cek apakah slot ke-i sampai i+duration-1 berada di hari yang sama
            # dan berurutan (kita asumsikan urutan list DB sudah benar blok per blok)
            start_slot = sorted_timeslots[i]
            end_slot = sorted_timeslots[i + duration - 1]

            # Valid jika hari sama. (Opsional: Cek selisih jam jika ada jeda istirahat)
            if start_slot.getHari() == end_slot.getHari():
                valid_indices.append(i)
        valid_start_indices[duration] = valid_indices

    conn.close()
    print(
        f"Loaded: {len(global_ruangans)} Ruangan, {len(global_pengajars)} Pengajar, {len(global_mks)} MK, {len(sorted_timeslots)} TimeSlots."
    )


def save_schedule_to_db(schedule: list[ScheduleItem]):
    """Menyimpan hasil ke tabel 'jadwal' sesuai skema jadwal_sa.sql."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Bersihkan tabel jadwal lama
    _ = cursor.execute("DELETE FROM jadwal")
    _ = cursor.execute(
        "DELETE FROM sqlite_sequence WHERE name='jadwal'"
    )  # Reset auto increment

    sql_insert = """
        INSERT INTO jadwal
        (hari, jam, matakuliah, jenis, sks, semester, kelas, ruangan, daring, pengajar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    data_to_insert: list[
        tuple[
            str,
            str,
            str | None,
            str | None,
            int | None,
            int | None,
            str,
            str,
            bool,
            str,
        ]
    ] = []

    for item in schedule:
        # Resolve data references
        ts_start = sorted_timeslots[item.timeslot_index]
        ts_end = sorted_timeslots[item.timeslot_index + item.mk.getSks() - 1]  # pyright: ignore[reportOperatorIssue]

        hari_str = Hari.getNama(ts_start.getHari()) or "Unknown"
        jam_str = f"{ts_start.getMulai()} - {ts_end.getSelesai()}"

        ruangan_nama = ""
        if item.is_daring:
            ruangan_nama = "ONLINE"
        elif item.ruangan_id:
            ruangan_nama = ruangan_map[item.ruangan_id].getNama()
        else:
            ruangan_nama = "Menunggu informasi"

        data_to_insert.append(
            (
                hari_str,
                jam_str,
                item.mk.getNama(),
                item.mk.getTipe(),
                item.mk.getSks(),
                item.mk.getSemester(),
                item.kelas_code,
                ruangan_nama,
                item.is_daring,
                item.pengajar.getNama(),
            )
        )

    _ = cursor.executemany(sql_insert, data_to_insert)
    conn.commit()
    conn.close()
    print("Jadwal berhasil disimpan ke database.")


# --- 3. LOGIKA ALGORITMA (SIMULATED ANNEALING) ---


def generate_initial_solution() -> list[ScheduleItem]:
    solution: list[ScheduleItem] = []
    uid_counter = 1

    # Pisahkan ID ruangan berdasarkan tipe untuk random picking
    ruang_teori: list[int] = [
        r.getId() for r in global_ruangans if r.getTipe() == "teori"
    ]
    ruang_praktek: list[int] = [
        r.getId() for r in global_ruangans if r.getTipe() == "praktek"
    ]

    # Validasi Data Kritis
    if not ruang_teori:
        print("WARNING: Tidak ada ruangan jenis 'teori' di Database!")
    if not ruang_praktek:
        print("WARNING: Tidak ada ruangan jenis 'praktek' di Database!")

    for mk in global_mks:
        # Loop sebanyak jumlah kelas (A, B, C...)
        num_kelas: int = mk.getKelas() or 1
        sks: int = mk.getSks() or 2

        valid_slots: list[int] = valid_start_indices.get(sks, [])
        if not valid_slots:
            print(
                f"CRITICAL: Tidak ada slot waktu valid untuk MK {mk.getNama()} ({sks} SKS)"
            )
            continue

        for i in range(num_kelas):
            kelas_code: str = chr(ord("A") + i)

            # Random initial state
            timeslot_idx: int = random.choice(valid_slots)

            # Tentukan ruangan
            r_id: int | None = None
            daring = False

            # Logic: Praktek prioritas offline di lab, Teori bisa online atau kelas
            if mk.getTipe() == "praktek":
                # Praktek WAJIB Offline. Jika tidak ada lab, ini akan jadi TBA (Issue data)
                if ruang_praktek:
                    r_id = random.choice(ruang_praktek)
                else:
                    # Jangan set daring = True. Biarkan None (TBA) agar user sadar data kurang
                    pass
            else:
                # Teori: 30% chance langsung online di awal
                if ruang_teori and random.random() > 0.3:
                    r_id = random.choice(ruang_teori)
                else:
                    daring = (
                        True  # Default ke Online jika random kena atau ruangan kosong
                    )

            item = ScheduleItem(
                uid=uid_counter,
                mk=mk,
                kelas_code=kelas_code,
                pengajar=mk.getPengampu(),  # Ambil dari MK struct # pyright: ignore[reportArgumentType]
                timeslot_index=timeslot_idx,
                ruangan_id=r_id,
                is_daring=daring,
            )
            solution.append(item)
            uid_counter += 1

    return solution


def calculate_cost(schedule: list[ScheduleItem]) -> float:
    cost = 0.0

    # Penalti Constants
    P_CRITICAL = 1000  # Bentrok Ruangan, Bentrok Pengajar
    P_STUDENT = 100  # Bentrok Mahasiswa (Semester sama, kelas sama)
    P_PREF = 10  # Preferensi Pengajar
    P_DARING = 5  # Penalti kecil untuk kelas online (agar memprioritaskan offline jika memungkinkan)

    # Dictionary untuk tracking collision
    # (ruangan_id, time_index) -> count
    room_occupancy: dict[tuple[int, int], int] = {}
    # (pengajar_id, time_index) -> count
    teacher_occupancy: dict[tuple[str, int], int] = {}
    # (semester, kelas, time_index) -> count (Asumsi mahasiswa satu kelas ambil paket yg sama)
    student_occupancy: dict[tuple[int, str, int], int] = {}

    for item in schedule:
        if item.is_daring:
            cost += P_DARING

        # Hitung range waktu yang ditempati (karena 1 MK bisa > 1 slot/SKS)
        duration = item.mk.getSks() or 1
        occupied_indices = range(item.timeslot_index, item.timeslot_index + duration)

        # Cek Preferensi Pengajar
        # Format preferensi di DB: "1, 2" (Hari yg dihindari). Kita perlu cek hari dari timeslot.
        current_hari = sorted_timeslots[item.timeslot_index].getHari()
        pref_waktu_str = item.pengajar.getWaktu()  # String "1,5" misalnya
        if pref_waktu_str:
            # Parse simple CSV
            hasil: list[str] = re.findall(r"\d+", pref_waktu_str)
            avoid_days = [int(x) for x in hasil]
            if current_hari in avoid_days:
                cost += P_PREF

        for idx in occupied_indices:
            # 1. Cek Bentrok Ruangan (Hanya jika tidak daring)
            if not item.is_daring and item.ruangan_id is not None:
                key_r: tuple[int, int] = (item.ruangan_id, idx)
                if key_r in room_occupancy:
                    cost += P_CRITICAL
                    room_occupancy[key_r] += 1
                else:
                    room_occupancy[key_r] = 1

            # 2. Cek Bentrok Pengajar
            # Pengajar tidak bisa mengajar 2 kelas berbeda di jam yang sama
            key_t = (item.pengajar.getId(), idx)
            if key_t in teacher_occupancy:
                cost += P_CRITICAL
                teacher_occupancy[key_t] += 1
            else:
                teacher_occupancy[key_t] = 1

            # 3. Cek Bentrok Mahasiswa
            # Asumsi: Mahasiswa Semester 3 Kelas A tidak bisa kuliah 2 MK di jam sama
            key_s: tuple[int, str, int] = (
                item.mk.getSemester(),  # pyright: ignore[reportAssignmentType]
                item.kelas_code,
                idx,
            )
            if key_s in student_occupancy:
                cost += P_STUDENT
                student_occupancy[key_s] += 1
            else:
                student_occupancy[key_s] = 1

    return cost


def get_neighbor(schedule: list[ScheduleItem]) -> list[ScheduleItem]:
    """Mengubah satu entitas jadwal secara acak."""
    # new_schedule: list[ScheduleItem] = copy.deepcopy(schedule)
    new_schedule: list[ScheduleItem] = [replace(item) for item in schedule]
    if not new_schedule:
        return new_schedule

    # Pilih satu item acak
    item: ScheduleItem = random.choice(new_schedule)

    ruang_teori: list[int] = [
        r.getId() for r in global_ruangans if r.getTipe() == "teori"
    ]
    ruang_praktek: list[int] = [
        r.getId() for r in global_ruangans if r.getTipe() == "praktek"
    ]

    # Random action
    action: float = random.random()

    if action < 0.5:
        # Ganti Waktu
        sks: int = item.mk.getSks() or 1
        valid_slots: list[int] = valid_start_indices.get(sks, [])
        if valid_slots:
            item.timeslot_index = random.choice(valid_slots)

    elif action < 0.8:
        # Ganti Ruangan
        if item.mk.getTipe() == "teori":
            # PERBAIKAN: Naikkan peluang switch ke Online menjadi 50:50
            # Ini memberi kesempatan algoritma "bernapas" jika ruangan penuh
            if random.random() < 0.5:
                item.is_daring = True
                item.ruangan_id = None
            else:
                item.is_daring = False
                if ruang_teori:
                    item.ruangan_id = random.choice(ruang_teori)
                else:
                    # Fallback jika tidak ada ruangan teori sama sekali: Paksa Online
                    item.is_daring = True
        else:
            # Praktek hanya boleh ganti Lab, TIDAK BOLEH Online
            if ruang_praktek:
                item.ruangan_id = random.choice(ruang_praktek)
                item.is_daring = False
            # Jika tidak ada ruang praktek, biarkan di state sebelumnya (atau error)

    # TODO: hapus
    else:
        # Swap pengajar (Hanya valid jika ada pengajar lain yang mampu mengampu -
        # Untuk saat ini diskip karena struktur MK mengikat 1 pengajar spesifik di DB Anda)
        # Bisa diimplementasikan jika ada tabel relasi many-to-many pengajar-mk
        pass

    return new_schedule


def simulated_annealing(
    max_iter: int = 5000,
    initial_temp: float = 1000.0,
    cooling_rate: float = 0.995,
    progress_callback: Callable[[int, float], None] | None = None,
) -> tuple[list[ScheduleItem], float]:
    print(f"Memulai Simulated Annealing ({max_iter} iterasi)...")

    current_solution: list[ScheduleItem] = generate_initial_solution()
    current_cost: float = calculate_cost(current_solution)

    best_solution: list[ScheduleItem] = current_solution
    best_cost: float = current_cost

    temp: float = initial_temp

    for i in range(max_iter):
        neighbor: list[ScheduleItem] = get_neighbor(current_solution)
        neighbor_cost: float = calculate_cost(neighbor)

        delta: float = neighbor_cost - current_cost

        # Acceptance probability
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_solution = neighbor
            current_cost = neighbor_cost

            if current_cost < best_cost:
                best_solution = current_solution
                best_cost = current_cost
                print(f"Iterasi {i}: New Best Cost = {best_cost}")

        # UPDATE: Panggil callback setiap X iterasi (misal setiap 100 iterasi agar tidak spamming signal)
        if progress_callback and i % 50 == 0:
            # Kirim data: (iterasi_sekarang, cost_terbaik_saat_ini)
            progress_callback(i, best_cost)

        temp *= cooling_rate

        if best_cost == 0:
            print("Solusi sempurna ditemukan (Cost 0)!")
            break

    return best_solution, best_cost


# --- 4. PRINTING UTILS ---


def print_result(schedule: list[ScheduleItem], cost: float):
    print("\n" + "=" * 60)
    print(f"HASIL AKHIR PENJADWALAN (Total Penalti: {cost})")
    print("=" * 60)

    # Sort agar enak dibaca: Hari -> Jam -> Semester
    schedule.sort(
        key=lambda x: (
            sorted_timeslots[x.timeslot_index].getHari(),
            sorted_timeslots[x.timeslot_index].getMulai(),
            x.mk.getSemester(),
        )
    )

    current_day = -1
    for item in schedule:
        ts: TimeSlot = sorted_timeslots[item.timeslot_index]
        ts_end: TimeSlot = sorted_timeslots[
            item.timeslot_index + (item.mk.getSks() or 1) - 1
        ]

        if ts.getHari() != current_day:
            current_day: int = ts.getHari()
            day_name: str = Hari.getNama(current_day)  # pyright: ignore[reportAssignmentType]
            print(f"\n--- {day_name} ---")

        lokasi: str = (
            "ONLINE"
            if item.is_daring
            else (
                ruangan_map[item.ruangan_id].getNama() if item.ruangan_id else "No Room"
            )
        )

        print(
            f"[{ts.getMulai()} - {ts_end.getSelesai()}] "
            + f"Sem{item.mk.getSemester()} | {item.mk.getNama()} ({item.kelas_code}) "
            + f"| {item.mk.getTipe().upper()} "  # pyright: ignore[reportOptionalMemberAccess]
            + f"| {item.pengajar.getNama()} "
            + f"| {lokasi}"
        )


def convert_to_struct_objects(schedule: list[ScheduleItem]) -> list[Jadwal]:
    """
    Mengonversi hasil internal algoritma (ScheduleItem) menjadi
    List of Jadwal Struct (QObject) yang siap dikonsumsi oleh GUI.
    """
    jadwal_objects: list[Jadwal] = []

    for item in schedule:
        # 1. Resolusi Waktu (Index -> TimeSlot Object)
        # Ambil slot awal dan akhir untuk mendapatkan rentang waktu
        ts_start: TimeSlot = sorted_timeslots[item.timeslot_index]
        ts_end: TimeSlot = sorted_timeslots[
            item.timeslot_index + (item.mk.getSks() or 1) - 1
        ]

        # Konversi ke String yang user-friendly
        hari_str: str = Hari.getNama(ts_start.getHari()) or "Unknown"
        jam_str: str = f"{ts_start.getMulai()} - {ts_end.getSelesai()}"

        # 2. Resolusi Ruangan
        nama_ruangan = ""
        if item.is_daring:
            nama_ruangan = "ONLINE"
        elif item.ruangan_id:
            # Ambil nama ruangan dari map global
            r: Ruangan | None = ruangan_map.get(item.ruangan_id)
            nama_ruangan = r.getNama() if r else "Unknown Room"
        else:
            nama_ruangan = "Menunggu informasi"

        # 3. Pembuatan Objek Jadwal (Sesuai definisi di struct_jadwal.py)
        # Perhatikan: struct Jadwal mewarisi QObject, jadi pastikan QApplication
        # sudah berjalan jika fungsi ini dipanggil di thread utama GUI.
        j = Jadwal(
            id=0,  # ID belum ada karena belum masuk DB, atau bisa diset -1
            hari=hari_str,
            jam=jam_str,
            matakuliah=item.mk.getNama() or "",
            jenis=item.mk.getTipe() or "",
            sks=item.mk.getSks() or 0,
            semester=item.mk.getSemester() or 0,
            kelas=item.kelas_code,
            ruangan=nama_ruangan,
            daring=item.is_daring,
            pengajar=item.pengajar.getNama(),
        )

        jadwal_objects.append(j)

    return jadwal_objects


# --- MAIN EXECUTION ---

if __name__ == "__main__":
    # 1. Load Data External
    load_data()

    if not global_mks:
        print("Data Mata Kuliah kosong. Pastikan database terisi.")
        exit()

    # 2. Run Algorithm
    final_sched, final_cost = simulated_annealing(max_iter=10000)

    # 3. Print & Save
    print_result(final_sched, final_cost)
    save_schedule_to_db(final_sched)
