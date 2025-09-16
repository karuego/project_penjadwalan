import sqlite3
from typing import List, Tuple, Optional
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path: str = "waktu_schedule.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database dengan tabel yang diperlukan"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Tabel untuk menyimpan timeslots
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS timeslots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hari TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(hari, start_time, end_time)
                )
            ''')

            # Tabel untuk log atau audit (opsional)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    timeslot_id INTEGER,
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()

    def get_connection(self):
        """Mendapatkan koneksi database"""
        return sqlite3.connect(self.db_path)

class TimeSlotValidator:
    @staticmethod
    def time_to_minutes(time_str: str) -> int:
        """Konversi waktu string ke menit"""
        try:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        except (ValueError, AttributeError):
            raise ValueError(f"Format waktu tidak valid: {time_str}")

    @staticmethod
    def is_overlap(start1: str, end1: str, start2: str, end2: str) -> bool:
        """Cek apakah dua rentang waktu overlap"""
        s1 = TimeSlotValidator.time_to_minutes(start1)
        e1 = TimeSlotValidator.time_to_minutes(end1)
        s2 = TimeSlotValidator.time_to_minutes(start2)
        e2 = TimeSlotValidator.time_to_minutes(end2)

        return s1 < e2 and e1 > s2

    @staticmethod
    def validate_time_format(time_str: str) -> bool:
        """Validasi format waktu HH:MM"""
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False

class TimeSlotManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.validator = TimeSlotValidator()

    def check_overlap_in_db(self, hari: str, start_time: str, end_time: str, exclude_id: int = None) -> bool:
        """
        Cek overlap dengan timeslot yang sudah ada di database
        Returns True jika overlap, False jika tidak
        """
        if not all([self.validator.validate_time_format(start_time),
                   self.validator.validate_time_format(end_time)]):
            raise ValueError("Format waktu tidak valid")

        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()

            query = '''
                SELECT start_time, end_time FROM timeslots
                WHERE hari = ? AND id != ?
            '''
            params = [hari, exclude_id or -1]

            cursor.execute(query, params)
            existing_slots = cursor.fetchall()

        for existing_start, existing_end in existing_slots:
            if self.validator.is_overlap(start_time, end_time, existing_start, existing_end):
                return True

        return False

    def add_timeslot(self, hari: str, start_time: str, end_time: str) -> Tuple[bool, int, str]:
        """
        Menambahkan timeslot baru ke database dengan validasi
        Returns: (success, timeslot_id, message)
        """
        try:
            # Validasi input
            if not all([hari, start_time, end_time]):
                return False, None, "Semua field harus diisi"

            if not self.validator.validate_time_format(start_time):
                return False, None, "Format start_time tidak valid (HH:MM)"

            if not self.validator.validate_time_format(end_time):
                return False, None, "Format end_time tidak valid (HH:MM)"

            # Cek overlap
            if self.check_overlap_in_db(hari, start_time, end_time):
                return False, None, f"Waktu overlap dengan timeslot yang sudah ada pada {hari}"

            # Insert ke database
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT INTO timeslots (hari, start_time, end_time)
                    VALUES (?, ?, ?)
                ''', (hari, start_time, end_time))

                timeslot_id = cursor.lastrowid

                # Log audit
                cursor.execute('''
                    INSERT INTO audit_log (action, timeslot_id, details)
                    VALUES (?, ?, ?)
                ''', ('CREATE', timeslot_id, f'Added timeslot {hari} {start_time}-{end_time}'))

                conn.commit()

            return True, timeslot_id, "Timeslot berhasil ditambahkan"

        except sqlite3.Error as e:
            return False, None, f"Database error: {str(e)}"
        except Exception as e:
            return False, None, f"Error: {str(e)}"

    def get_all_timeslots(self, hari: str = None) -> List[Tuple]:
        """Mendapatkan semua timeslots, bisa difilter oleh hari"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()

            if hari:
                cursor.execute('''
                    SELECT id, hari, start_time, end_time, created_at
                    FROM timeslots
                    WHERE hari = ?
                    ORDER BY hari, start_time
                ''', (hari,))
            else:
                cursor.execute('''
                    SELECT id, hari, start_time, end_time, created_at
                    FROM timeslots
                    ORDER BY hari, start_time
                ''')

            return cursor.fetchall()

    def get_timeslot_by_id(self, timeslot_id: int) -> Optional[Tuple]:
        """Mendapatkan timeslot berdasarkan ID"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, hari, start_time, end_time, created_at
                FROM timeslots
                WHERE id = ?
            ''', (timeslot_id,))

            return cursor.fetchone()

    def delete_timeslot(self, timeslot_id: int) -> Tuple[bool, str]:
        """Menghapus timeslot"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # Dapatkan info timeslot untuk log
                cursor.execute('SELECT hari, start_time, end_time FROM timeslots WHERE id = ?', (timeslot_id,))
                timeslot = cursor.fetchone()

                if not timeslot:
                    return False, "Timeslot tidak ditemukan"

                # Hapus timeslot
                cursor.execute('DELETE FROM timeslots WHERE id = ?', (timeslot_id,))

                # Log audit
                cursor.execute('''
                    INSERT INTO audit_log (action, timeslot_id, details)
                    VALUES (?, ?, ?)
                ''', ('DELETE', timeslot_id, f'Deleted timeslot {timeslot[0]} {timeslot[1]}-{timeslot[2]}'))

                conn.commit()

            return True, "Timeslot berhasil dihapus"

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

    def clear_all_timeslots(self) -> Tuple[bool, str]:
        """Menghapus semua timeslots"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM timeslots')
                cursor.execute('DELETE FROM audit_log')
                conn.commit()

            return True, "Semua timeslots berhasil dihapus"
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

class ScheduleGenerator:
    def __init__(self, timeslot_manager: TimeSlotManager):
        self.manager = timeslot_manager

    def generate_schedule(self) -> Tuple[int, List[Tuple[bool, int, str]]]:
        """
        Generate jadwal dan simpan ke database
        Returns: (total_generated, results)
        """
        hari_list = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
        results = []
        total_generated = 0

        for hari in hari_list:
            for jam in range(8, 17):
                for menit in [0, 45]:
                    if jam == 12:  # Skip jam istirahat
                        continue

                    # Hitung waktu
                    jam_mulai_obj = (jam * 60) + menit
                    jam_selesai_obj = jam_mulai_obj + 45
                    start_h, start_m = divmod(jam_mulai_obj, 60)
                    end_h, end_m = divmod(jam_selesai_obj, 60)

                    start_time = f"{start_h:02d}:{start_m:02d}"
                    end_time = f"{end_h:02d}:{end_m:02d}"

                    # Tambahkan ke database
                    success, timeslot_id, message = self.manager.add_timeslot(hari, start_time, end_time)
                    results.append((success, timeslot_id, message))

                    if success:
                        total_generated += 1

        return total_generated, results

# Contoh penggunaan dan testing
def main():
    # Initialize database
    db_manager = DatabaseManager("waktu_schedule.db")
    timeslot_manager = TimeSlotManager(db_manager)
    schedule_generator = ScheduleGenerator(timeslot_manager)

    # Bersihkan database sebelumnya (opsional)
    timeslot_manager.clear_all_timeslots()

    print("=== GENERATING SCHEDULE ===")
    total_generated, results = schedule_generator.generate_schedule()

    print(f"Total timeslot generated: {total_generated}")
    print(f"Total attempts: {len(results)}")

    # Tampilkan hasil
    successes = [r for r in results if r[0]]
    failures = [r for r in results if not r[0]]

    print(f"\nSuccess: {len(successes)}")
    print(f"Failed (overlap): {len(failures)}")

    if failures:
        print("\nFailed entries (overlap):")
        for failure in failures[:5]:  # Tampilkan 5 pertama saja
            print(f"  - {failure[2]}")

    # Tampilkan jadwal yang berhasil disimpan
    print("\n=== SCHEDULE IN DATABASE ===")
    all_timeslots = timeslot_manager.get_all_timeslots()

    for timeslot in all_timeslots:
        print(f"ID: {timeslot[0]}, Hari: {timeslot[1]}, Waktu: {timeslot[2]} - {timeslot[3]}")

    # Test menambahkan timeslot yang overlap
    print("\n=== TESTING OVERLAP VALIDATION ===")
    success, timeslot_id, message = timeslot_manager.add_timeslot('Senin', '08:30', '09:15')
    print(f"Tambah timeslot overlap: {'Success' if success else 'Failed'} - {message}")

    # Test menambahkan timeslot yang valid
    success, timeslot_id, message = timeslot_manager.add_timeslot('Senin', '17:00', '17:45')
    print(f"Tambah timeslot valid: {'Success' if success else 'Failed'} - {message}")

def export_to_csv(db_path: str = "waktu_schedule.db"):
    """Export data ke CSV untuk analisis"""
    import csv

    db_manager = DatabaseManager(db_path)
    timeslot_manager = TimeSlotManager(db_manager)

    timeslots = timeslot_manager.get_all_timeslots()

    with open('schedule_export.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Hari', 'Start Time', 'End Time', 'Created At'])

        for timeslot in timeslots:
            writer.writerow(timeslot)

    print("Data berhasil diexport ke schedule_export.csv")

if __name__ == "__main__":
    main()
    # export_to_csv()  # Uncomment untuk export CSV
