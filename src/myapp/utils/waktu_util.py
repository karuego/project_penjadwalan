import typing
import sqlite3
from datetime import datetime
from .database import Database
from .hari import Hari
from .struct_waktu import TimeSlot


class TimeSlotManager:
    def __init__(self, db: Database):
        self.db: Database = db
        self.validator: TimeSlotValidator = TimeSlotValidator()

    def check_overlap_in_db(
        self, hari: int, start_time: str, end_time: str, exclude_id: int | None = None
    ) -> bool:
        """
        Cek overlap dengan timeslot yang sudah ada di database
        Returns True jika overlap, False jika tidak
        """
        if not all(
            [
                self.validator.validate_time_format(start_time),
                self.validator.validate_time_format(end_time),
            ]
        ):
            raise ValueError("Format waktu tidak valid")

        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            query = """
                SELECT mulai, selesai FROM timeslots
                WHERE hari = ? AND id != ?
            """
            params = [hari, exclude_id or -1]

            _ = cursor.execute(query, params)
            existing_slots: list[typing.Any] = cursor.fetchall()

        for existing_start, existing_end in existing_slots:  # pyright: ignore[reportAny]
            if self.validator.is_overlap(
                start_time,
                end_time,
                existing_start,  # pyright: ignore[reportAny]
                existing_end,  # pyright: ignore[reportAny]
            ):
                return True

        return False

    def add_timeslot(
        self, hari: int, start_time: str, end_time: str
    ) -> tuple[bool, int | None, str]:
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
                return (
                    False,
                    None,
                    f"Waktu overlap dengan timeslot yang sudah ada pada {Hari.getNama(hari)}",
                )

            # Insert ke database
            with self.db.get_connection() as conn:
                cursor: sqlite3.Cursor = conn.cursor()

                _ = cursor.execute(
                    """
                    INSERT INTO timeslots (hari, mulai, selesai)
                    VALUES (?, ?, ?)
                """,
                    (hari, start_time, end_time),
                )

                timeslot_id = cursor.lastrowid

                conn.commit()

            return True, timeslot_id, "Timeslot berhasil ditambahkan"

        except sqlite3.Error as e:
            return False, None, f"Database error: {str(e)}"
        except Exception as e:
            return False, None, f"Error: {str(e)}"

    def get_all_timeslots(self, hari: int | None = None) -> list[TimeSlot]:
        """Mendapatkan semua timeslots, bisa difilter oleh hari"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            if hari:
                _ = cursor.execute(
                    """
                    SELECT id, hari, mulai, selesai
                    FROM timeslots
                    WHERE hari = ?
                    ORDER BY hari, mulai
                """,
                    (hari,),
                )
            else:
                _ = cursor.execute("""
                    SELECT id, hari, mulai, selesai
                    FROM timeslots
                    ORDER BY hari, mulai
                """)

            # return cursor.fetchall()
            res: list[tuple[int, int, str, str]] | None = cursor.fetchall()
            if not res:
                return []

            waktu: list[TimeSlot] = []
            for item in res:
                waktu.append(
                    TimeSlot(id=item[0], hari=item[1], mulai=item[2], selesai=item[3])
                )
            return waktu

    def get_timeslot_by_id(self, timeslot_id: int) -> TimeSlot | None:
        """Mendapatkan timeslot berdasarkan ID"""
        with self.db.get_connection() as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            _ = cursor.execute(
                """
                SELECT id, hari, mulai, selesai
                FROM timeslots
                WHERE id = ?
            """,
                (timeslot_id,),
            )

            res = typing.cast(tuple[int, int, str, str] | None, cursor.fetchone())
            if not res:
                return None
            return TimeSlot(id=res[0], hari=res[1], mulai=res[2], selesai=res[3])

    def delete_timeslot(self, timeslot_id: int) -> tuple[bool, str]:
        """Menghapus timeslot"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()

                # Dapatkan info timeslot untuk log
                _ = cursor.execute(
                    "SELECT hari, mulai, selesai FROM timeslots WHERE id = ?",
                    (timeslot_id,),
                )

                res: tuple[int, str, str] | None = cursor.fetchone()  # pyright: ignore[reportAny]

                if not res:
                    return False, "Timeslot tidak ditemukan"

                # Hapus timeslot
                _ = cursor.execute("DELETE FROM timeslots WHERE id = ?", (timeslot_id,))

                conn.commit()

            return True, "Timeslot berhasil dihapus"

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

    def clear_all_timeslots(self) -> tuple[bool, str]:
        """Menghapus semua timeslots"""
        try:
            with self.db.get_connection() as conn:
                cursor: sqlite3.Cursor = conn.cursor()
                _ = cursor.execute("DELETE FROM timeslots")
                conn.commit()

            return True, "Semua timeslots berhasil dihapus"
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"


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
