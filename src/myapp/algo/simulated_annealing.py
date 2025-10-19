import random
import math
import copy
from dataclasses import dataclass, field
from typing import List, Dict, Set

# --- 1. DEFINISI STRUKTUR DATA (Berdasarkan DBML) ---
# Menggunakan dataclasses untuk merepresentasikan setiap tabel agar lebih terstruktur.

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
    # Menambahkan informasi tambahan untuk memudahkan evaluasi
    semester: int
    jenis_mk: str # 'teori' atau 'praktek'

# --- 2. DATA SAMPEL ---
# Data ini digunakan untuk simulasi. Anda bisa menggantinya dengan data dari database.

# Ruangan
ruangans = [
    Ruangan(id=1, nama='R-101', jenis='teori'),
    Ruangan(id=2, nama='R-102', jenis='teori'),
    Ruangan(id=3, nama='Lab-Kom A', jenis='praktek'),
    Ruangan(id=4, nama='Lab-Kom B', jenis='praktek'),
]
ruangan_teori_ids = [r.id for r in ruangans if r.jenis == 'teori']
ruangan_praktek_ids = [r.id for r in ruangans if r.jenis == 'praktek']
ruangan_map = {r.id: r for r in ruangans}

# Dosen
dosens = [
    Dosen(id=1, nama='Dr. Budi'),
    Dosen(id=2, nama='Dr. Ani'),
    Dosen(id=3, nama='Dr. Candra'),
]
dosen_map = {d.id: d for d in dosens}

# Waktu (Senin & Selasa, masing-masing 4 slot)
waktus = [
    Waktu(id=1, hari='Senin', jam_mulai='08:00', jam_selesai='10:00'),
    Waktu(id=2, hari='Senin', jam_mulai='10:00', jam_selesai='12:00'),
    Waktu(id=3, hari='Senin', jam_mulai='13:00', jam_selesai='15:00'),
    Waktu(id=4, hari='Senin', jam_mulai='15:00', jam_selesai='17:00'),
    Waktu(id=5, hari='Selasa', jam_mulai='08:00', jam_selesai='10:00'),
    Waktu(id=6, hari='Selasa', jam_mulai='10:00', jam_selesai='12:00'),
    Waktu(id=7, hari='Selasa', jam_mulai='13:00', jam_selesai='15:00'),
    Waktu(id=8, hari='Selasa', jam_mulai='15:00', jam_selesai='17:00'),
]
waktu_ids = [w.id for w in waktus]
waktu_map = {w.id: w for w in waktus}


# Mata Kuliah
mata_kuliahs = [
    MataKuliah(id=1, nama='Basis Data', semester=3, jumlah_kelas=2, jenis='teori'),
    MataKuliah(id=2, nama='Praktikum Basis Data', semester=3, jumlah_kelas=2, jenis='praktek'),
    MataKuliah(id=3, nama='Kecerdasan Buatan', semester=5, jumlah_kelas=1, jenis='teori'),
    MataKuliah(id=4, nama='Jaringan Komputer', semester=5, jumlah_kelas=1, jenis='teori'),
]
mata_kuliah_map = {mk.id: mk for mk in mata_kuliahs}

# Pengampu (Dosen yang mengajar mata kuliah)
pengampus = [
    Pengampu(mata_kuliah_id=1, dosen_id=1), # Basis Data oleh Dr. Budi
    Pengampu(mata_kuliah_id=2, dosen_id=1), # Praktikum Basis Data oleh Dr. Budi
    Pengampu(mata_kuliah_id=3, dosen_id=2), # AI oleh Dr. Ani
    Pengampu(mata_kuliah_id=4, dosen_id=3), # Jarkom oleh Dr. Candra
]
# Membuat map untuk pencarian dosen pengampu dengan cepat
pengampu_map = {p.mata_kuliah_id: p.dosen_id for p in pengampus}

# Preferensi Dosen (waktu yang dihindari)
preferensi_dosens = [
    PreferensiDosen(dosen_id=2, waktu_id=1), # Dr. Ani tidak mau mengajar Senin pagi
    PreferensiDosen(dosen_id=3, waktu_id=8), # Dr. Candra tidak mau mengajar Selasa sore
]
# Membuat set untuk pengecekan preferensi yang efisien
preferensi_set = {(p.dosen_id, p.waktu_id) for p in preferensi_dosens}


# --- 3. FUNGSI UNTUK MEMBUAT JADWAL AWAL ---

def generate_initial_solution() -> List[JadwalItem]:
    """
    Membuat jadwal awal secara acak dengan memastikan jenis ruangan sesuai dengan jenis mata kuliah.
    """
    initial_schedule = []
    
    # Buat daftar semua kelas yang harus dijadwalkan
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

    # Acak penempatan ke waktu dan ruangan
    for kelas_info in list_kelas_untuk_dijadwalkan:
        waktu_terpilih = random.choice(waktu_ids)
        
        # Pilih ruangan sesuai jenis mata kuliah
        if kelas_info['jenis_mk'] == 'teori':
            ruangan_terpilih = random.choice(ruangan_teori_ids)
        else: # praktek
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

def calculate_cost(schedule: List[JadwalItem]) -> int:
    """
    Menghitung total biaya (penalti) dari sebuah jadwal.
    Semakin kecil biayanya, semakin baik jadwalnya.
    """
    cost = 0
    
    # Bobot penalti: Hard constraint harus jauh lebih besar dari soft constraint
    PENALTI_HARD = 100
    PENALTI_SOFT = 1

    # Pengecekan Hard Constraints (konflik)
    # Gunakan set untuk mendeteksi duplikasi dengan efisien
    ruangan_waktu_check = set()
    dosen_waktu_check = set()
    mahasiswa_waktu_check = set() # Mahasiswa diwakili oleh semester

    for item in schedule:
        # 1. Konflik Ruangan: Satu ruangan tidak bisa dipakai >1 kelas di waktu yang sama
        if (item.ruangan_id, item.waktu_id) in ruangan_waktu_check:
            cost += PENALTI_HARD
        else:
            ruangan_waktu_check.add((item.ruangan_id, item.waktu_id))

        # 2. Konflik Dosen: Satu dosen tidak bisa mengajar >1 kelas di waktu yang sama
        if (item.dosen_id, item.waktu_id) in dosen_waktu_check:
            cost += PENALTI_HARD
        else:
            dosen_waktu_check.add((item.dosen_id, item.waktu_id))
            
        # 3. Konflik Mahasiswa: Mahasiswa satu semester tidak bisa ada >1 kelas di waktu yang sama
        if (item.semester, item.waktu_id) in mahasiswa_waktu_check:
            cost += PENALTI_HARD
        else:
            mahasiswa_waktu_check.add((item.semester, item.waktu_id))

    # Pengecekan Soft Constraints (preferensi)
    for item in schedule:
        # 4. Preferensi Dosen: Dosen menghindari waktu tertentu
        if (item.dosen_id, item.waktu_id) in preferensi_set:
            cost += PENALTI_SOFT
            
    return cost

# --- 5. FUNGSI UNTUK MENDAPATKAN SOLUSI TETANGGA ---

def get_neighbor_solution(schedule: List[JadwalItem]) -> List[JadwalItem]:
    """
    Membuat solusi baru (tetangga) dengan membuat sedikit perubahan acak pada jadwal saat ini.
    """
    neighbor = copy.deepcopy(schedule)
    
    # Pilih satu item jadwal secara acak untuk diubah
    if not neighbor:
        return neighbor
        
    item_to_change_idx = random.randrange(len(neighbor))
    item_to_change = neighbor[item_to_change_idx]
    
    # Opsi perubahan: ganti waktu atau ganti ruangan
    if random.random() < 0.5:
        # Ganti waktu
        new_waktu_id = random.choice(waktu_ids)
        item_to_change.waktu_id = new_waktu_id
    else:
        # Ganti ruangan (sesuai jenis MK)
        if item_to_change.jenis_mk == 'teori':
            new_ruangan_id = random.choice(ruangan_teori_ids)
        else:
            new_ruangan_id = random.choice(ruangan_praktek_ids)
        item_to_change.ruangan_id = new_ruangan_id
        
    return neighbor

# --- 6. ALGORITMA SIMULATED ANNEALING ---

def simulated_annealing(initial_temp: float, cooling_rate: float, stopping_temp: float, max_iterations: int):
    """
    Fungsi utama untuk menjalankan algoritma Simulated Annealing.
    """
    print("Memulai proses optimasi dengan Simulated Annealing...")
    
    # 1. Inisialisasi
    current_solution = generate_initial_solution()
    current_cost = calculate_cost(current_solution)
    
    best_solution = copy.deepcopy(current_solution)
    best_cost = current_cost
    
    temperature = initial_temp
    iteration = 0
    
    print(f"Biaya Awal: {current_cost}")

    # 2. Loop utama
    while temperature > stopping_temp and iteration < max_iterations:
        # 3. Dapatkan tetangga
        neighbor_solution = get_neighbor_solution(current_solution)
        neighbor_cost = calculate_cost(neighbor_solution)
        
        # 4. Hitung perbedaan biaya
        cost_difference = neighbor_cost - current_cost
        
        # 5. Tentukan apakah akan menerima solusi baru
        if cost_difference < 0: # Solusi baru lebih baik, selalu terima
            current_solution = neighbor_solution
            current_cost = neighbor_cost
        else:
            # Solusi baru lebih buruk, terima dengan probabilitas tertentu
            acceptance_probability = math.exp(-cost_difference / temperature)
            if random.random() < acceptance_probability:
                current_solution = neighbor_solution
                current_cost = neighbor_cost
        
        # 6. Update solusi terbaik yang pernah ditemukan
        if current_cost < best_cost:
            best_solution = copy.deepcopy(current_solution)
            best_cost = current_cost
            print(f"Iterasi {iteration}: Ditemukan solusi lebih baik dengan biaya -> {best_cost}")

        # 7. Turunkan suhu
        temperature *= cooling_rate
        iteration += 1
        
        if iteration % 1000 == 0:
            print(f"Iterasi {iteration}, Suhu: {temperature:.2f}, Biaya Saat Ini: {current_cost}, Biaya Terbaik: {best_cost}")

    print("\nProses optimasi selesai.")
    return best_solution, best_cost

# --- 7. FUNGSI UNTUK MENAMPILKAN HASIL ---

def print_schedule(schedule: List[JadwalItem], cost: int):
    """
    Mencetak hasil jadwal dalam format yang mudah dibaca.
    """
    print("\n======================================")
    print("      HASIL PENJADWALAN OPTIMAL     ")
    print("======================================")
    print(f"Total Biaya (Penalti): {cost}")
    if cost == 0:
        print("Status: Optimal (Tidak ada konflik ditemukan)")
    else:
        print("Status: Sub-optimal (Masih ada konflik atau pelanggaran preferensi)")
    print("--------------------------------------\n")

    # Mengelompokkan jadwal berdasarkan hari
    schedule_by_day = {w.hari: [] for w in waktus}
    for item in schedule:
        hari = waktu_map[item.waktu_id].hari
        schedule_by_day[hari].append(item)

    for hari, items in schedule_by_day.items():
        if not items: continue
        print(f"--- HARI: {hari.upper()} ---")
        # Urutkan berdasarkan jam mulai
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
    # Parameter Simulated Annealing (bisa disesuaikan)
    INITIAL_TEMPERATURE = 1000.0  # Suhu awal yang tinggi
    COOLING_RATE = 0.995         # Tingkat pendinginan (mendekati 1)
    STOPPING_TEMPERATURE = 0.1   # Suhu berhenti
    MAX_ITERATIONS = 50000       # Batas iterasi untuk mencegah loop tak terbatas

    # Jalankan algoritma
    final_schedule, final_cost = simulated_annealing(
        INITIAL_TEMPERATURE,
        COOLING_RATE,
        STOPPING_TEMPERATURE,
        MAX_ITERATIONS
    )
    
    # Tampilkan hasil
    print_schedule(final_schedule, final_cost)

