from .timeslot_manager import TimeSlotManager
from .waktu import Hari


class ScheduleGenerator:
    def __init__(self, timeslot_manager: TimeSlotManager):
        self.manager: TimeSlotManager = timeslot_manager

    def generate_schedule(self) -> tuple[int, list[tuple[bool, int | None, str]]]:
        """
        Generate jadwal dan simpan ke database
        Returns: (total_generated, results)
        """
        hari_list: list[str] = Hari.getAll()[:5]
        results: list[tuple[bool, int | None, str]] = []
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
                    success, timeslot_id, message = self.manager.add_timeslot(
                        Hari.getId(hari), start_time, end_time
                    )
                    results.append((success, timeslot_id, message))

                    if success:
                        total_generated += 1

        return total_generated, results
