from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from datetime import time, datetime

@dataclass
class TimeSlot:
    id: int
    hari: str
    start_time: str
    end_time: str

    def to_time_objects(self):
        """Mengonversi string waktu ke objek time"""
        start_obj = datetime.strptime(self.start_time, '%H:%M').time()
        end_obj = datetime.strptime(self.end_time, '%H:%M').time()
        return start_obj, end_obj

    def to_minutes(self):
        """Mengonversi waktu ke total menit sejak 00:00"""
        start_h, start_m = map(int, self.start_time.split(':'))
        end_h, end_m = map(int, self.end_time.split(':'))
        return start_h * 60 + start_m, end_h * 60 + end_m


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



class WaktuValidator:
    def __init__(self):
        self.registered_times: Dict[str, List[TimeSlot]] = {}
        self.next_id = 1

    def time_to_minutes(self, time_str: str) -> int:
        """Mengkonversi string waktu ke menit"""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    def is_time_overlap(self, start1: str, end1: str, start2: str, end2: str) -> bool:
        """
        Mengecek apakah dua rentang waktu overlap
        Returns True jika overlap, False jika tidak
        """
        start1_min = self.time_to_minutes(start1)
        end1_min = self.time_to_minutes(end1)
        start2_min = self.time_to_minutes(start2)
        end2_min = self.time_to_minutes(end2)

        # Cek semua kemungkinan overlap
        return (
            (start1_min <  end2_min   and end1_min   >  start2_min) or # Overlap parsial
            (start1_min >= start2_min and start1_min <  end2_min)   or # Mulai di tengah
            (end1_min > start2_min    and end1_min   <= end2_min)   or # Selesai di tengah
            (start1_min <= start2_min and end1_min   >= end2_min)      # Mengcover seluruhnya
        )

    def can_add_time(self, hari: str, start_time: str, end_time: str) -> bool:
        """Mengecek apakah waktu baru bisa ditambahkan tanpa overlap"""
        if hari not in self.registered_times:
            return True

        for existing_slot in self.registered_times[hari]:
            if self.is_time_overlap(
                start_time, end_time,
                existing_slot.start_time, existing_slot.end_time
            ):
                return False

        return True

    def add_time_slot(self, hari: str, start_time: str, end_time: str) -> Tuple[bool, TimeSlot]:
        """
        Menambahkan timeslot baru jika valid
        Returns: (success, timeslot_object)
        """
        if not self.can_add_time(hari, start_time, end_time):
            return False, None

        timeslot = TimeSlot(
            id=self.next_id,
            hari=hari,
            start_time=start_time,
            end_time=end_time
        )

        if hari not in self.registered_times:
            self.registered_times[hari] = []

        self.registered_times[hari].append(timeslot)
        self.next_id += 1

        return True, timeslot

    def get_all_timeslots(self) -> List[TimeSlot]:
        """Mendapatkan semua timeslot yang terdaftar"""
        all_slots = []
        for day_slots in self.registered_times.values():
            all_slots.extend(day_slots)
        return sorted(all_slots, key=lambda x: (x.hari, x.start_time))

    def get_timeslots_by_day(self, hari: str) -> List[TimeSlot]:
        """Mendapatkan timeslot untuk  hari tertentu"""
        return sorted(self.registered_times.get(hari, []), key=lambda x: x.start_time)

    def clear_all(self):
        """Menghapus semua timeslot"""
        self.registered_times.clear()
        self.next_id = 1


class WaktuGenerator:
    def __init__(self):
        self.validator = WaktuValidator()

    def generate_schedule(self) -> List[TimeSlot]:
        """Generate jadwal waktu"""
        hari_list = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']

        for hari in hari_list:
            for jam in range(8, 17):
                for menit in [0, 45]:
                    if jam == 12: # Skip jam istirahat
                        continue

                    # Hitung waktu mulai dan selesai
                    jam_mulai_obj = (jam * 60) + menit
                    jam_selesai_obj = jam_mulai_obj + 45

                    start_h, start_m = divmod(jam_mulai_obj, 60)
                    end_h, end_m = divmod(jam_selesai_obj, 60)

                    start_time = f"{start_h:02d}:{start_m:02d}"
                    end_time = f"{end_h:02d}:{end_m:02d}"

                    # Coba tambahkan timeslot
                    self.validator.add_time_slot(hari, start_time, end_time)

        return self.validator.get_all_timeslots()

    def generate_schedule_2(self) -> List[TimeSlot]:
        durasi = 45
        waktu_mulai = '08:00'

        # waktu_data = []
        # waktu_id = 1

        for hari in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']:
            jam, menit = map(int, waktu_mulai.split(':'))

            while jam < 17:
                jam_mulai_obj = jam * 60 + menit
                jam_selesai_obj = jam_mulai_obj + 45

                start_h, start_m = divmod(jam_mulai_obj, 60)
                end_h, end_m = divmod(jam_selesai_obj, 60)

                jam = end_h
                menit = end_m

                if jam == 12: continue

                start_time = f"{start_h:02d}:{start_m:02d}"
                end_time = f"{end_h:02d}:{end_m:02d}"

                # waktu_data.append((waktu_id, hari, start_time, end_time))
                # waktu_id += 1
                self.validator.add_time_slot(hari, start_time, end_time)

        return self.validator.get_all_timeslots()




def test_overlap_scenarios():
    """Mencoba berbagai skenario overlap"""
    validator = WaktuValidator()

    test_cases = [
        (('08:00', '08:45'), ('08:30', '09:15'), True),  # Overlap parsial
        (('09:00', '09:45'), ('09:45', '10:30'), False), # Bersebelahan, tidak overlap
        (('10:00', '10:45'), ('09:30', '10:15'), True),  # Overlap
        (('11:00', '11:45'), ('11:00', '11:45'), True),  # Sama persis
        (('13:00', '13:45'), ('12:30', '13:15'), True),  # Overlap
        (('14:00', '14:45'), ('15:00', '15:45'), False), # Terpisah
    ]

    print("\n=== TEST OVER SCENARIOS ===")
    for i, (time1, time2, should_overlap) in enumerate(test_cases, 1):
        result = validator.is_time_overlap(time1[0], time1[1], time2[0], time2[1])
        status = "PASS" if result == should_overlap else "FAIL"
        print(f"Test {i}: {time1} vs {time2} -> {result} (expected: {should_overlap}) [{status}]")


# Contoh penggunaan
def main():
    # Contoh 1: Generate jadwal normal
    print('=== GENERATE JADWAL NORMAL ===')
    generator = WaktuGenerator()
    schedule = generator.generate_schedule_2()

    for timeslot in schedule:
        print(
            f"ID: {timeslot.id}, Hari: {timeslot.hari}, "
            f"Waktu: {timeslot.start_time} - {timeslot.end_time}"
        )

    print(f"\nTotal timeslot: {len(schedule)}")

    # Contoh 2: Validasi manual
    print("\n=== VALIDASI MANUAL ===")
    validator = WaktuValidator()

    # Tambah timeslot valid
    success1, slot1 = validator.add_time_slot('Senin', '08:00', '08:45')
    print(f"Tambah 08:00-08:45: {'Berhasil' if success1 else 'Gagal'}")

    # Coba tambah yang overlap
    success2, slot2 = validator.add_time_slot('Senin', '08:30', '09:15')
    print(f"Tambah 08:30-09:15: {'Berhasil' if success2 else 'Gagal'} (harusnya gagal)")

    # Tambah yang tidak overlap
    success3, slot3 = validator.add_time_slot('Senin', '09:00', '09:45')
    print(f"Tambah 09:00-09:45: {'Berhasil' if success3 else 'Gagal'} (harusnya berhasil)")

    # Contoh 3: Cek timeslot per hari
    print('\n=== TIMESLOT SENIN ===')
    senin_slots = validator.get_timeslots_by_day('Senin')
    for slot in senin_slots:
        print(f'{slot.start_time} - {slot.end_time}')

if __name__ == '__main__':
    main()
    test_overlap_scenarios()
