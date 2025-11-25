import os
import sqlite3
from result import Result, Ok, Err

# from .schedule_generator import ScheduleGenerator
# from .waktu_util import TimeSlotManager
from .struct_pengajar import Pengajar
from .struct_matakuliah import MataKuliah
from .struct_ruangan import Ruangan

DB_FILE: str = "database.sqlite3.db"

class Database:
    def __init__(self) -> None:
        if not self.is_exist():
            self.init_database()

    def init_database(self) -> None:
        """Initialize database dengan tabel yang diperlukan"""

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Tabel untuk menyimpan timeslots
            _ = cursor.execute("""
                CREATE TABLE IF NOT EXISTS timeslots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hari INTEGER NOT NULL,
                    mulai TEXT NOT NULL,
                    selesai TEXT NOT NULL,
                    UNIQUE(hari, mulai, selesai)
                )
            """)

            _ = cursor.execute("""
                CREATE TABLE pengajar (
                    id TEXT PRIMARY KEY NOT NULL,
                    nama TEXT NOT NULL,
                    jenis TEXT NOT NULL DEFAULT 'dosen',
                    preferensi_waktu TEXT
                )
            """)

            _ = cursor.execute("""
                CREATE TABLE mata_kuliah (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    semester INTEGER NOT NULL
                )
            """)

            _ = cursor.execute("""
                CREATE TABLE ruangan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL UNIQUE,
                    jenis TEXT NOT NULL DEFAULT 'teori'
                )
            """)

            _ = cursor.execute("""
                CREATE TABLE komponen_mk (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mata_kuliah_id INTEGER NOT NULL,
                    nama_komponen TEXT NOT NULL,
                    durasi_blok INTEGER NOT NULL,
                    jenis TEXT NOT NULL DEFAULT 'teori',
                    jumlah_kelas INTEGER NOT NULL,
                    jumlah_sesi_praktikum INTEGER NOT NULL DEFAULT 1,
                    FOREIGN KEY (mata_kuliah_id) REFERENCES mata_kuliah(id)
                )
            """)

            _ = cursor.execute("""
                CREATE TABLE pengampu (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pengajar_id INTEGER,
                    komponen_mk_id INTEGER NOT NULL,
                    FOREIGN KEY (pengajar_id) REFERENCES pengajar(id),
                    FOREIGN KEY (komponen_mk_id) REFERENCES komponen_mk(id)
                )
            """)

            _ = cursor.execute("""
                CREATE TABLE jadwal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    komponen_mk_id INTEGER NOT NULL,
                    pengajar_id INTEGER NOT NULL,
                    kelas CHAR NOT NULL,
                    sesi_ke INTEGER NOT NULL,
                    waktu_id_start INTEGER NOT NULL,
                    durasi_blok INTEGER NOT NULL,
                    ruangan_id INTEGER NULL,
                    daring BOOLEAN NOT NULL DEFAULT FALSE,
                    FOREIGN KEY (komponen_mk_id) REFERENCES komponen_mk(id),
                    FOREIGN KEY (pengajar_id) REFERENCES pengajar(id),
                    FOREIGN KEY (waktu_id_start) REFERENCES waktu(id)
                )
            """)

            conn.commit()

    def get_connection(self) -> sqlite3.Connection:
        """Mendapatkan koneksi database"""
        return sqlite3.connect(DB_FILE)

    def is_exist(self) -> bool:
        """Cek apakah file database sudah ada"""
        return os.path.exists(DB_FILE)

    def get_all_pengajar(self) -> list[Pengajar]:
        """Mendapatkan semua pengajar dari database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            _ = cursor.execute("SELECT * FROM pengajar ORDER BY nama")
            res: list[tuple[str, str, str, str]] | None = cursor.fetchall()
            if not res:
                return []

            pengajar: list[Pengajar] = []
            for item in res:
                pengajar.append(
                    Pengajar(id=item[0], nama=item[1], tipe=item[2], waktu=item[3])
                )
            return pengajar

    def get_pengajar_by_id(self, id: str) -> Result[Pengajar, str]:
        """Mendapatkan pengajar berdasarkan ID"""
        with self.get_connection() as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            _ = cursor.execute(
                """
                    SELECT id, nama, jenis, preferensi_waktu
                    FROM pengajar
                    WHERE id = ?
                """,
                (id,),
            )

            res: tuple[str, str, str, str] | None = cursor.fetchone() # pyright: ignore[reportAny]
            if not res:
                return Err("Pengajar tidak ditemukan")

            return Ok(Pengajar(id=res[0], nama=res[1], tipe=res[2], waktu=res[3]))

    def delete_pengajar(self, id: str) -> Result[str, str]:
        """Menghapus data pengajar"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                _ = cursor.execute(
                    "SELECT id, nama FROM pengajar WHERE id = ?",
                    (id,),
                )

                res: tuple[str, str] | None = cursor.fetchone()  # pyright: ignore[reportAny]

                if not res:
                    return Err("Pengajar tidak ditemukan")

                _ = cursor.execute("DELETE FROM pengajar WHERE id = ?", (id,))

                conn.commit()

            return Ok("Pengajar berhasil dihapus")

        except sqlite3.Error as e:
            return Err(f"Database error: {str(e)}")
        except Exception as e:
            return Err(f"Error: {str(e)}")

    def update_pengajar(self, id: str, pengajar: Pengajar) -> Result[str, str]:
        """memperbarui data pengajar"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                _ = cursor.execute(
                    "SELECT id, nama FROM pengajar WHERE id = ?",
                    (id,),
                )

                res: tuple[str, str] | None = cursor.fetchone()  # pyright: ignore[reportAny]

                if not res:
                    return Err("Pengajar tidak ditemukan")

                _ = cursor.execute(
                    """
                        UPDATE pengajar
                        SET id = ?, nama = ?, jenis = ?, preferensi_waktu = ?
                        WHERE id = ?
                    """,
                    (
                        pengajar.getId(),
                        pengajar.getNama(),
                        pengajar.getTipe(),
                        pengajar.getWaktu(),
                        id,
                    )
                )

                conn.commit()

            return Ok("Pengajar berhasil diperbarui")

        except sqlite3.Error as e:
            return Err(f"Database error: {str(e)}")
        except Exception as e:
            return Err(f"Error: {str(e)}")

    def clear_all_pengajar(self) -> Result[str, str]:
        """Menghapus semua pengajar"""
        try:
            with self.get_connection() as conn:
                cursor: sqlite3.Cursor = conn.cursor()
                _ = cursor.execute("DELETE FROM pengajar")
                conn.commit()

            return Ok("Semua pengajar berhasil dihapus")
        except sqlite3.Error as e:
            return Err(f"Database error: {str(e)}")
        except Exception as e:
            return Err(f"Error: {str(e)}")

    def get_all_matakuliah(self) -> list[MataKuliah]:
        """Mendapatkan semua mata kuliah dari database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            _ = cursor.execute("SELECT id, nama, jenis, sks, semester, jumlah_kelas, pengajar_id FROM mata_kuliah ORDER BY nama")
            res: list[tuple[int, str, str, int, int, int, str]] | None = cursor.fetchall()
            if not res:
                return []

            matkul: list[MataKuliah] = []
            for item in res:
                pengajar_res: Result[Pengajar, str] = self.get_pengajar_by_id(item[6])
                if pengajar_res.is_err():
                    continue
                pengajar: Pengajar = pengajar_res.unwrap()
                matkul.append(
                    MataKuliah(id=item[0], nama=item[1], tipe=item[2], sks=item[3], semester=item[4], kelas=item[5], pengampu=pengajar)
                )
            return matkul

    def get_matakuliah_by_id(self, id: int) -> Result[MataKuliah, str]:
        """Mendapatkan mata kuliah berdasarkan ID"""
        with self.get_connection() as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            _ = cursor.execute(
                """
                    SELECT id, nama, jenis, sks, semester, jumlah_kelas, pengajar_id
                    FROM mata_kuliah
                    WHERE id = ?
                """,
                (id,),
            )

            res: tuple[int, str, str, int, int, int, str] | None = cursor.fetchone() # pyright: ignore[reportAny]
            if not res:
                return Err("Pengajar tidak ditemukan")

            pengajar_res: Result[Pengajar, str] = self.get_pengajar_by_id(res[6])
            if pengajar_res.is_err():
                return Err("Gagal memproses")

            pengajar: Pengajar = pengajar_res.unwrap()

            return Ok(MataKuliah(id=res[0], nama=res[1], tipe=res[2], sks=res[3], semester=res[4], kelas=res[5], pengampu=pengajar))

    def delete_matakuliah(self, id: int) -> Result[str, str]:
        """Menghapus data mata kuliah"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                _ = cursor.execute(
                    "SELECT id, nama, jenis, sks, semester, jumlah_kelas, pengajar_id FROM mata_kuliah WHERE id = ?",
                    (id,),
                )

                res: tuple[int, str, str, int, int, int, str] | None = cursor.fetchone()  # pyright: ignore[reportAny]
                if not res:
                    return Err("Mata Kuliah tidak ditemukan di database")

                _ = cursor.execute("DELETE FROM mata_kuliah WHERE id = ?", (id,))
                conn.commit()

            return Ok("Mata Kuliah berhasil dihapus")

        except sqlite3.Error as e:
            return Err(f"Database error: {str(e)}")
        except Exception as e:
            return Err(f"Error: {str(e)}")

    def update_matakuliah(self, id: int, matkul: MataKuliah) -> Result[str, str]:
        """memperbarui data mata kuliah"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                _ = cursor.execute(
                    "SELECT nama, semester, jumlah_kelas, pengajar_id FROM mata_kuliah WHERE id = ?",
                    (id,),
                )

                res: tuple[str, int, int, str] | None = cursor.fetchone()  # pyright: ignore[reportAny]
                if not res:
                    return Err("Pengajar tidak ditemukan")

                _ = cursor.execute(
                    """
                        UPDATE mata_kuliah
                        SET nama = ?, semester = ?, jumlah_kelas = ?, pengajar_id = ?
                        WHERE id = ?
                    """,
                    (
                        matkul.getNama(),
                        matkul.getSemester(),
                        matkul.getKelas(),
                        matkul.getPengampu().getId(), # pyright: ignore[reportOptionalMemberAccess]
                        id,
                    )
                )

                conn.commit()

            return Ok("Mata kuliah berhasil diperbarui")

        except sqlite3.Error as e:
            return Err(f"Database error: {str(e)}")
        except Exception as e:
            return Err(f"Error: {str(e)}")

    def clear_all_matakuliah(self) -> Result[str, str]:
        """Menghapus semua mata kuliah"""
        try:
            with self.get_connection() as conn:
                cursor: sqlite3.Cursor = conn.cursor()
                _ = cursor.execute("DELETE FROM mata_kuliah")
                conn.commit()

            return Ok("Semua mata kuliah berhasil dihapus")
        except sqlite3.Error as e:
            return Err(f"Database error: {str(e)}")
        except Exception as e:
            return Err(f"Error: {str(e)}")

    def get_all_ruangan(self) -> list[Ruangan]:
        """Mendapatkan semua ruangan dari database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            _ = cursor.execute("SELECT id, nama, jenis FROM ruangan ORDER BY nama")
            res: list[tuple[int, str, str]] | None = cursor.fetchall()
            if not res:
                return []

            ruangan: list[Ruangan] = []
            for item in res:
                ruangan.append(
                    Ruangan(id=item[0], nama=item[1], tipe=item[2])
                )
            return ruangan

    def get_ruangan_by_id(self, id: int) -> Result[Ruangan, str]:
        """Mendapatkan ruangan berdasarkan ID"""
        with self.get_connection() as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            _ = cursor.execute("SELECT id, nama, jenis FROM ruangan WHERE id = ?", (id,))

            res: tuple[int, str, str] | None = cursor.fetchone() # pyright: ignore[reportAny]
            if not res:
                return Err("Ruangan tidak ditemukan")

            return Ok(Ruangan(id=res[0], nama=res[1], tipe=res[2]))

    def delete_ruangan(self, id: int) -> Result[str, str]:
        """Menghapus data ruangan"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                _ = cursor.execute("SELECT id, nama, jenis FROM ruangan WHERE id = ?", (id,))

                res: tuple[int, str, str] | None = cursor.fetchone()  # pyright: ignore[reportAny]
                if not res:
                    return Err("Ruangan tidak ditemukan di database")

                _ = cursor.execute("DELETE FROM ruangan WHERE id = ?", (id,))
                conn.commit()

            return Ok("Ruangan berhasil dihapus dari database")

        except sqlite3.Error as e:
            return Err(f"Database error: {str(e)}")
        except Exception as e:
            return Err(f"Error tidak terduga: {str(e)}")

    def update_ruangan(self, id: int, ruang: Ruangan) -> Result[str, str]:
        """memperbarui data ruangan"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                _ = cursor.execute("SELECT nama, jenis FROM ruangan WHERE id = ?", (id,))

                res: tuple[str, str] | None = cursor.fetchone()  # pyright: ignore[reportAny]
                if not res:
                    return Err("Ruangan tidak ditemukan")

                _ = cursor.execute("UPDATE ruangan SET nama = ?, jenis = ? WHERE id = ?", (
                    ruang.getNama(),
                    ruang.getTipe(),
                    id
                ))

                conn.commit()

            return Ok("Data ruangan berhasil diperbarui")

        except sqlite3.Error as e:
            return Err(f"Database error: {str(e)}")
        except Exception as e:
            return Err(f"Error tidak terduga: {str(e)}")

    def clear_all_ruangan(self) -> Result[str, str]:
        """Menghapus semua ruangan dari database"""
        try:
            with self.get_connection() as conn:
                cursor: sqlite3.Cursor = conn.cursor()
                _ = cursor.execute("DELETE FROM ruangan")
                conn.commit()

            return Ok("Semua ruangan berhasil dihapus")
        except sqlite3.Error as e:
            return Err(f"Database error: {str(e)}")
        except Exception as e:
            return Err(f"Error tidak terduga: {str(e)}")
