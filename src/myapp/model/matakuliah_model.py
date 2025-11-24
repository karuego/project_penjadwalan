import re
import sqlite3
import typing
from result import Result, Ok, Err, is_ok, is_err
from maybe import Maybe, Some, Nothing

from PySide6.QtCore import (
    QAbstractListModel,
    QByteArray,
    QModelIndex,
    QObject,
    QPersistentModelIndex,
    Qt,
    Slot,
)
from .pengajar_model import PengajarModel
from utils import ( # pyright: ignore[reportImplicitRelativeImport]
    Database,
    MataKuliah,
    Pengajar,
)
import log # pyright: ignore[reportImplicitRelativeImport]


class MataKuliahModel(QAbstractListModel):
    ID_ROLE: int = int(Qt.ItemDataRole.UserRole) + 1
    NAMA_ROLE: int = int(Qt.ItemDataRole.UserRole) + 2
    TIPE_ROLE: int = int(Qt.ItemDataRole.UserRole) + 3
    SEMESTER_ROLE: int = int(Qt.ItemDataRole.UserRole) + 4
    SKS_ROLE: int = int(Qt.ItemDataRole.UserRole) + 5
    JUMLAH_KELAS_ROLE: int = int(Qt.ItemDataRole.UserRole) + 6
    JUMLAH_SESI_PRAKTIKUM_ROLE: int = int(Qt.ItemDataRole.UserRole) + 7
    PENGAMPU_ROLE: int = int(Qt.ItemDataRole.UserRole) + 8

    _filter_query: str = ""     # pyright: ignore[reportRedeclaration]
    _filter_tipe: str = "semua" # pyright: ignore[reportRedeclaration]

    def __init__(self, db: Database, parent: QObject | None = None):
        super().__init__(parent)
        self.db: Database = db
        self._all_data: list[MataKuliah] = []
        self._filtered: list[MataKuliah] = []

    @typing.override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> int | str | dict[str, str] | None:
        """Mengembalikan data untuk item dan role tertentu."""

        if not index.isValid():
            return None

        matkul: MataKuliah = self._filtered[index.row()]

        return {
            self.ID_ROLE:                      matkul.getId(),
            self.NAMA_ROLE:                    matkul.getNama(),
            self.TIPE_ROLE:                    matkul.getTipe(),
            self.SEMESTER_ROLE:                matkul.getSemester(),
            self.SKS_ROLE:                     matkul.getSks(),
            self.JUMLAH_KELAS_ROLE:            matkul.getKelas(),
            self.JUMLAH_SESI_PRAKTIKUM_ROLE:   matkul.getSesi(),
            self.PENGAMPU_ROLE:                matkul.getPengampu().asDict()
        }.get(role, None)

    @typing.override
    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex | None = None,
    ) -> int:
        """Mengembalikan jumlah total item dalam model."""
        if parent is None:
            parent = QModelIndex()

        # return len(self._all_data)
        return len(self._filtered)

    @typing.override
    def roleNames(self) -> dict[int, QByteArray]:
        """Menghubungkan roles dengan nama yang akan digunakan di QML."""
        return {
            self.ID_ROLE:                     QByteArray(b"id_"),
            self.NAMA_ROLE:                   QByteArray(b"nama"),
            self.TIPE_ROLE:                   QByteArray(b"tipe"),
            self.SEMESTER_ROLE:               QByteArray(b"semester"),
            self.SKS_ROLE:                    QByteArray(b"sks"),
            self.JUMLAH_KELAS_ROLE:           QByteArray(b"kelas"),
            self.JUMLAH_SESI_PRAKTIKUM_ROLE:  QByteArray(b"sesi")
        }

    def setDataMataKuliah(self, data: list[MataKuliah]) -> None:
        self._all_data = list[MataKuliah](data)
        self._filtered = list[MataKuliah](data)

    def addMataKuliahToList(self, matkul: MataKuliah) -> None:
        """Method untuk menambahkan mata kuliah ke database."""
        self._all_data.append(matkul)
        self._filtered.append(matkul)
        self.fnFilter(self._filter_query, self._filter_tipe)

    def addMataKuliahToDatabase(self, matkul: MataKuliah) -> tuple[bool, str]:
        """
        Menambahkan mata kuliah baru ke database dengan validasi
        Returns: (success, message)
        """
        conn = self.db.get_connection()
        cursor: sqlite3.Cursor = conn.cursor()
        _ = cursor.execute("PRAGMA foreign_keys = ON;")

        try:
            # Validasi input
            if not all([
                matkul.getNama(),
                matkul.getTipe(),
                matkul.getSemester(),
                matkul.getSks(),
                matkul.getKelas(),
                matkul.getSesi()
            ]):
                return False, "Field Nama, Jenis, Semester, SKS, Jumlah kelas, dan Jumlah sesi praktikum harus diisi"


            query = "SELECT nama FROM mata_kuliah WHERE id = ?"
            params: list[int] = [matkul.getId()]

            _ = cursor.execute(query, params)
            data_lama: str | None = typing.cast(str|None, cursor.fetchone())

            if data_lama is not None:
                return False, f'Mata kuliah "{matkul.getNama()}" sudah ada.'

            _ = cursor.execute(
                """
                    INSERT INTO mata_kuliah (nama, semester)
                    VALUES (?, ?)
                """,
                (matkul.getNama(), matkul.getSemester()),
            )

            matkul_id_baru: int | None = cursor.lastrowid
            log.info(f"Kategori '{matkul.getNama()}' dibuat dengan ID: {matkul_id_baru}")

            new_matkul: dict[str, dict[str, str|int]] = {
                'teori': {
                    'nama': matkul.getNama(),
                    'bobot': matkul.getSks()
                },
                'praktek': {
                    'nama': '',
                    'bobot': 0
                }
            }
            if matkul.getTipe() == "praktek":
                new_matkul['praktek']['nama'] = f"Praktikum {matkul.getNama()}"
                new_matkul['praktek']['bobot'] = 1
                new_matkul['teori']['bobot'] = int(new_matkul['teori']['bobot']) - 1

            for jenis, komponen in new_matkul.items():
                if jenis == "praktek" and not komponen['nama']:
                    continue

                _ = cursor.execute(
                    """
                        INSERT INTO komponen_mk (mata_kuliah_id, nama_komponen, durasi_blok, jenis, jumlah_kelas, jumlah_sesi_praktikum)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (matkul_id_baru, komponen['nama'], komponen['bobot'], jenis, matkul.getKelas(), matkul.getSesi()),
                )

            conn.commit()
            return True, "Mata Kuliah berhasil ditambahkan"

        except sqlite3.Error as e:
            conn.rollback()
            log.info(f"Gagal! Transaksi dibatalkan. Error: {e}")
            return False, f"Database error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()

    def fnAdd(
        self,
        id: int,
        nama: str,
        tipe: str,
        semester: int,
        sks: int,
        kelas: int,
        sesi: int,
        pengajar_id: str
    ) -> tuple[bool, str]:
        """Method untuk menambahkan mata kuliah baru ke model."""
        success = True
        message = "Berhasil"

        pengajar_model: PengajarModel = PengajarModel(self.db)
        pengajar_res: Result[Pengajar, str] = pengajar_model.DB_get_pengajar_by_id(pengajar_id)
        if is_err(pengajar_res):
            return False, pengajar_res.unwrap_err()
        pengajar: Pengajar = pengajar_res.unwrap()

        matkul: MataKuliah = MataKuliah(
            id,
            nama.strip(),
            tipe.strip(),
            semester,
            sks,
            kelas,
            sesi,
            pengajar_id
        )

        p: Result[Pengajar, str] = PengajarModel(self.db).DB_get_pengajar_by_id(pengajar_id)
        if p.is_ok():
            matkul.setPengampu(p.unwrap())

        success, message = self.addMataKuliahToDatabase(matkul)
        if not success:
            return success, message

        self.addMataKuliahToList(matkul)
        return success, message

    @Slot(int, str, str, int, int, int, int, str, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def add(
        self,
        id: int,
        nama: str,
        tipe: str,
        semester: int,
        sks: int,
        kelas: int,
        sesi: int,
        pengajar_id: str,
    ) -> dict[str, bool | str]:
        """Menambahkan mata kuliah baru ke model dan database."""
        success, message = self.fnAdd(id, nama, tipe, semester, sks, kelas, sesi, pengajar_id)
        return {"success": success, "message": message}

    def fnUpdate(
        self, old_id: str, new_id: str, nama: str, tipe: str, waktu: str
    ) -> tuple[bool, str]:
        """Method untuk mengubah data pengajar yang ada di model."""
        success: bool = False
        message: str = "Gagal memperbarui data pengajar"

        # filtered_data: list[Pengajar] = []
        for index, pengajar in enumerate[MataKuliah](self._all_data):
            if pengajar.getId() != old_id:
                continue

            res: Result[str, str] = self.DB_update_pengajar(old_id, Pengajar(new_id, nama, tipe, waktu))
            if is_err(res):
                return False, res.unwrap_err()

            success = True
            message = res.unwrap()

            if pengajar.getId() != new_id:
                pengajar.setId(new_id)

            pengajar.setNama(nama)
            _ = pengajar.setTipe(tipe)
            pengajar.setWaktu(waktu)

            # Beri tahu QML View bahwa data pada index tersebut telah berubah untuk role tertentu
            roles_to_notify: list[int] = [PengajarModel.ID_ROLE, PengajarModel.NAMA_ROLE, PengajarModel.TIPE_ROLE, PengajarModel.WAKTU_ROLE]
            model_index: QModelIndex = self.index(index, 0)
            self.dataChanged.emit(model_index, model_index, roles_to_notify)

            break

        self.fnFilter(self._filter_query, self._filter_tipe)
        return success, message

    @Slot(str, str, str, str, str, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def update(
        self, old_id: str, new_id: str, nama: str, tipe: str, waktu: str
    ) -> dict[str, bool | str]:
        """Memperbarui item berdasarkan ID dan memancarkan sinyal dataChanged."""
        success, message = self.fnUpdate(old_id, new_id, nama, tipe, waktu)
        return {"success": success, "message": message}

    def getIndexById(self, id: str) -> int:
        # for i, item in enumerate(self._all_data):
        for i, item in enumerate(self._filtered):
            if item.getId() == id:
                return i

        return -1

    def fnGetById(self, id: str) -> Pengajar | None:
        """Mengambil data pengajar berdasarkan id."""
        for pengajar in self._all_data:
            if pengajar.getId() == id:
                return pengajar

        return None

    @Slot(str, result=QObject)  # pyright: ignore[reportAny]
    def getById(self, id: str) -> Pengajar | None:
        return self.fnGetById(id)

    def fnGetByIndex(self, index: int) -> Pengajar | None:
        """
        Method untuk mengambil data pengajar berdasarkan index.
        """
        # if 0 <= index < self.rowCount():
        if 0 <= index < len(self._all_data):
            return self._all_data[index]

        return None

    @Slot(int, result=QObject)  # pyright: ignore[reportAny]
    def getByIndex(self, index: int) -> Pengajar | None:
        return self.fnGetByIndex(index)

    @Slot(int, result=QObject)  # pyright: ignore[reportAny]
    def getFilteredByIndex(self, index: int) -> Pengajar | None:
        if 0 <= index < self.rowCount():
            return self._filtered[index]

        return None

    def fnRemoveByIndex(self, index: int) -> None:
        """
        Method untuk menghapus pengajar berdasarkan index.
        """
        # Pastikan index valid
        if 0 <= index < self.rowCount():
            # Memberi tahu view bahwa kita akan menghapus baris
            self.beginRemoveRows(QModelIndex(), index, index)

            # Hapus data dari list internal
            del self._all_data[index]

            # Memberi tahu view bahwa penghapusan baris telah selesai
            self.endRemoveRows()

    @Slot(int)  # pyright: ignore[reportAny]
    def removeByIndex(self, index: int) -> None:
        self.fnRemoveByIndex(index)

    def fnRemoveById(self, id: str) -> dict[str, bool | str]:
        """Method untuk menghapus pengajar berdasarkan id key."""
        index: int = self.getIndexById(id)

        self.beginRemoveRows(QModelIndex(), index, index)
        res: Result[str, str] = self.DB_delete_pengajar(id)
        if is_err(res):
            self.endRemoveRows()
            return {"success": False, "message": res.unwrap_err()}


        del self._all_data[index]
        del self._filtered[index]
        self.endRemoveRows()

        return {"success": True, "message": res.unwrap()}

    @Slot(str, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def removeById(self, id: str) -> dict[str, bool | str]:
        return self.fnRemoveById(id)

    def fnFilter(self, query: str, tipe: str) -> None:
        """
        Filter data berdasarkan nama dan tipe.
        """

        q: str = query.strip().lower()
        t: str = tipe.strip().lower()

        self._filter_query: str = q
        self._filter_tipe: str = t

        self.beginResetModel()

        pattern: re.Pattern[str] | None = None
        try:
            pattern = re.compile(q, re.IGNORECASE)
        except re.error:
            pattern = None  # Abaikan regex yg tdk valdi

        # Filter data
        def cocok(p: Pengajar):
            nama_cocok = True
            tipe_cocok = True

            if pattern:
                nama_cocok = bool(pattern.search(p.getNama().lower()))
            if t != "semua":
                tipe_cocok = p.getTipe().lower() == t

            return nama_cocok and tipe_cocok

        self._filtered = []
        for pengajar in self._all_data:
            if cocok(pengajar):
                self._filtered.append(pengajar)

        # self._filtered = [
        #     pengajar
        #     for pengajar in self._all_data
        #     if (q in pengajar.getNama().lower())
        #     and (t == "semua" or pengajar.getTipe().lower() == t)
        # ]

        self.endResetModel()

    @Slot(str, str)  # pyright: ignore[reportAny]
    def filter(self, query: str, tipe: str) -> None:
        self.fnFilter(query, tipe)

    # @Slot(str, str, str, str, str)
    # def update(
    #     self,
    #     prev_id: str | None = None,
    #     id: str | None = None,
    #     nama: str | None = None,
    #     tipe: str | None = None,
    #     waktu: str | None = None,
    # ) -> None:
    #     if prev_id is None:
    #         return

    #     for i, pengajar in enumerate(self._all_data):
    #         if pengajar.getId() == prev_id:
    #             if id is not None:
    #                 pengajar.setId(id)
    #             if nama is not None:
    #                 pengajar.setNama(nama)
    #             if tipe is not None:
    #                 pengajar.setTipe(tipe)
    #             if waktu is not None:
    #                 pengajar.setWaktu(waktu)

    #             # top = self.index(row, 0)
    #             # bottom = self.index(row, 0)
    #             # self.dataChanged.emit(top, bottom, [])

    #             self.dataChanged.emit(self.index(i), self.index(i))
    #             break

    def loadDatabase(self) -> None:
        semua_pengajar: list[Pengajar] = self.DB_get_all_pengajar()
        for pengajar in semua_pengajar:
            self.addPengajarToList(pengajar)

    def DB_get_all_pengajar(self) -> list[Pengajar]:
        """Mendapatkan semua pengajar"""
        with self.db.get_connection() as conn:
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

    def DB_get_pengajar_by_id(self, id: int) -> Result[Pengajar, str]:
        """Mendapatkan pengajar berdasarkan ID"""
        with self.db.get_connection() as conn:
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

    def DB_delete_pengajar(self, id: str) -> Result[str, str]:
        """Menghapus data pengajar"""
        try:
            with self.db.get_connection() as conn:
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

    def DB_update_pengajar(self, id: str, pengajar: Pengajar) -> Result[str, str]:
        """memperbarui data pengajar"""
        try:
            with self.db.get_connection() as conn:
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

    def DB_clear_all_pengajar(self) -> Result[str, str]:
        """Menghapus semua pengajar"""
        try:
            with self.db.get_connection() as conn:
                cursor: sqlite3.Cursor = conn.cursor()
                _ = cursor.execute("DELETE FROM pengajar")
                conn.commit()

            return Ok("Semua timeslots berhasil dihapus")
        except sqlite3.Error as e:
            return Err(f"Database error: {str(e)}")
        except Exception as e:
            return Err(f"Error: {str(e)}")
