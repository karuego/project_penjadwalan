import sqlite3


class DatabaseManager:
    def __init__(self, db_path: str = "waktu_schedule.db") -> None:
        self.db_path: str = db_path
        # self.init_database()

    def init_database(self) -> None:
        """Initialize database dengan tabel yang diperlukan"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Tabel untuk menyimpan timeslots
            _ = cursor.execute("""
                CREATE TABLE IF NOT EXISTS timeslots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hari INTEGER NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(hari, start_time, end_time)
                )
            """)

            # Tabel untuk log atau audit (opsional)
            _ = cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    timeslot_id INTEGER,
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()

    def get_connection(self):
        """Mendapatkan koneksi database"""
        return sqlite3.connect(self.db_path)
