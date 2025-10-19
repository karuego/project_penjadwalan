from datetime import datetime


class TimeSlotValidator:
    @staticmethod
    def time_to_minutes(time_str: str) -> int:
        """Konversi waktu string ke menit"""
        try:
            hours, minutes = map(int, time_str.split(":"))
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
            _ = datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
