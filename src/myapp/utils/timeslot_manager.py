import sqlite3
import typing
from .database_manager import DatabaseManager
from .timeslot_validator import TimeSlotValidator
from .waktu import Hari, TimeSlot


class TimeSlotManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager: DatabaseManager = db_manager
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

        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()

            query = """
                SELECT start_time, end_time FROM timeslots
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
            with self.db_manager.get_connection() as conn:
                cursor: sqlite3.Cursor = conn.cursor()

                _ = cursor.execute(
                    """
                    INSERT INTO timeslots (hari, start_time, end_time)
                    VALUES (?, ?, ?)
                """,
                    (hari, start_time, end_time),
                )

                timeslot_id = cursor.lastrowid

                # Log audit
                _ = cursor.execute(
                    """
                    INSERT INTO audit_log (action, timeslot_id, details)
                    VALUES (?, ?, ?)
                """,
                    (
                        "CREATE",
                        timeslot_id,
                        f"Added timeslot {Hari.getNama(hari)} {start_time}-{end_time}",
                    ),
                )

                conn.commit()

            return True, timeslot_id, "Timeslot berhasil ditambahkan"

        except sqlite3.Error as e:
            return False, None, f"Database error: {str(e)}"
        except Exception as e:
            return False, None, f"Error: {str(e)}"

    def get_all_timeslots(self, hari: int | None = None) -> list[TimeSlot]:
        """Mendapatkan semua timeslots, bisa difilter oleh hari"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()

            if hari:
                _ = cursor.execute(
                    """
                    SELECT id, hari, start_time, end_time, created_at
                    FROM timeslots
                    WHERE hari = ?
                    ORDER BY hari, start_time
                """,
                    (hari,),
                )
            else:
                _ = cursor.execute("""
                    SELECT id, hari, start_time, end_time, created_at
                    FROM timeslots
                    ORDER BY hari, start_time
                """)

            # return cursor.fetchall()
            res: list[tuple[int, int, str, str, str]] | None = cursor.fetchall()
            if not res:
                return []
            return [TimeSlot(*row) for row in res]

    def get_timeslot_by_id(self, timeslot_id: int) -> TimeSlot | None:
        """Mendapatkan timeslot berdasarkan ID"""
        with self.db_manager.get_connection() as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            _ = cursor.execute(
                """
                SELECT id, hari, start_time, end_time, created_at
                FROM timeslots
                WHERE id = ?
            """,
                (timeslot_id,),
            )

            res = typing.cast(tuple[int, int, str, str, str] | None, cursor.fetchone())
            if not res:
                return None
            return TimeSlot(
                id=res[0], hari=res[1], mulai=res[2], selesai=res[3], createdAt=res[4]
            )

    def delete_timeslot(self, timeslot_id: int) -> tuple[bool, str]:
        """Menghapus timeslot"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()

                # Dapatkan info timeslot untuk log
                _ = cursor.execute(
                    "SELECT hari, start_time, end_time FROM timeslots WHERE id = ?",
                    (timeslot_id,),
                )

                res: tuple[int, str, str] | None = cursor.fetchone()

                if not res:
                    return False, "Timeslot tidak ditemukan"

                timeslot = TimeSlot(hari=res[0], mulai=res[1], selesai=res[2])

                # Hapus timeslot
                _ = cursor.execute("DELETE FROM timeslots WHERE id = ?", (timeslot_id,))

                # Log audit
                _ = cursor.execute(
                    """
                    INSERT INTO audit_log (action, timeslot_id, details)
                    VALUES (?, ?, ?)
                """,
                    (
                        "DELETE",
                        timeslot_id,
                        f"Deleted timeslot {timeslot.hari} {timeslot.mulai}-{timeslot.selesai}",
                    ),
                )

                conn.commit()

            return True, "Timeslot berhasil dihapus"

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

    def clear_all_timeslots(self) -> tuple[bool, str]:
        """Menghapus semua timeslots"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor: sqlite3.Cursor = conn.cursor()
                _ = cursor.execute("DELETE FROM timeslots")
                _ = cursor.execute("DELETE FROM audit_log")
                conn.commit()

            return True, "Semua timeslots berhasil dihapus"
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
