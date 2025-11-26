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
from myapp.utils import (
    Database,
    MataKuliah,
    Pengajar,
)
import myapp.log


class MataKuliahModel(QAbstractListModel):
    ID_ROLE: int = int(Qt.ItemDataRole.UserRole) + 1
    NAMA_ROLE: int = int(Qt.ItemDataRole.UserRole) + 2
    TIPE_ROLE: int = int(Qt.ItemDataRole.UserRole) + 3
    SKS_ROLE: int = int(Qt.ItemDataRole.UserRole) + 4
    SEMESTER_ROLE: int = int(Qt.ItemDataRole.UserRole) + 5
    JUMLAH_KELAS_ROLE: int = int(Qt.ItemDataRole.UserRole) + 6
    PENGAMPU_ROLE: int = int(Qt.ItemDataRole.UserRole) + 7

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
        pengampu: Pengajar = matkul.getPengampu() or Pengajar()

        return {
            self.ID_ROLE:            matkul.getId(),
            self.NAMA_ROLE:          matkul.getNama(),
            self.TIPE_ROLE:          matkul.getTipe(),
            self.SKS_ROLE:           matkul.getSks(),
            self.SEMESTER_ROLE:      matkul.getSemester(),
            self.JUMLAH_KELAS_ROLE:  matkul.getKelas(),
            self.PENGAMPU_ROLE:      pengampu.asDict()
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
            self.ID_ROLE:            QByteArray(b"id_"),
            self.NAMA_ROLE:          QByteArray(b"nama"),
            self.TIPE_ROLE:          QByteArray(b"tipe"),
            self.SKS_ROLE:           QByteArray(b"sks"),
            self.SEMESTER_ROLE:      QByteArray(b"semester"),
            self.JUMLAH_KELAS_ROLE:  QByteArray(b"kelas"),
            self.PENGAMPU_ROLE:      QByteArray(b"pengampu"),
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
                matkul.getSks(),
                matkul.getSemester(),
                matkul.getKelas(),
                matkul.getPengampu()
            ]):
                return False, "Field Nama, Jenis, SKS, Semester, Jumlah kelas, dan Pengampu harus diisi"

            query = "SELECT nama FROM mata_kuliah WHERE nama LIKE ?"
            _ = cursor.execute(query, (f"%{matkul.getNama()}%",))
            data_lama: str | None = typing.cast(str|None, cursor.fetchone())

            if data_lama is not None:
                return False, f'Mata kuliah "{matkul.getNama()}" sudah ada.'

            _ = cursor.execute(
                """
                    INSERT INTO mata_kuliah (nama, jenis, sks, semester, jumlah_kelas, pengajar_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    matkul.getNama(),
                    matkul.getTipe(),
                    matkul.getSks(),
                    matkul.getSemester(),
                    matkul.getKelas(),
                    matkul.getPengampu().getId() # pyright: ignore[reportOptionalMemberAccess]
                )
            )

            matkul_id_baru: int | None = cursor.lastrowid
            if not matkul_id_baru:
                log.info("Gagal menambahkan mata kuliah")
                return False, "Gagal menambahkan mata Kuliah"

            log.info(f"Mata Kuliah '{matkul.getNama()}' dibuat dengan ID: {matkul_id_baru}")
            matkul.setId(matkul_id_baru)

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
        nama: str,
        tipe: str,
        sks: int,
        semester: int,
        kelas: int,
        pengajar_teori_id: str,
        pengajar_praktek_id: str,
    ) -> tuple[bool, str]:
        """Method untuk menambahkan mata kuliah baru ke model."""
        success = True
        message = "Berhasil"

        pengajar_model: PengajarModel = PengajarModel(self.db)
        pengajar_teori_res: Result[Pengajar, str] = pengajar_model.db.get_pengajar_by_id(pengajar_teori_id)
        if is_err(pengajar_teori_res):
            return False, pengajar_teori_res.unwrap_err()
        pengajar_teori: Pengajar = pengajar_teori_res.unwrap()

        new_matkul: dict[str, dict[str, str|int|Pengajar]] = {
            'teori': {
                'nama': nama.strip(),
                'bobot': sks,
                'pengampu': pengajar_teori
            },
            'praktek': {
                'nama': '',
                'bobot': 0,
                'pengampu': Pengajar()
            }
        }

        if tipe == "praktek":
            new_matkul['teori']['bobot'] = new_matkul['teori']['bobot'] - 1 # pyright: ignore[reportOperatorIssue]
            new_matkul['praktek']['nama'] = f"Praktikum {nama.strip()}"
            new_matkul['praktek']['bobot'] = 1

            pengajar_praktek_res: Result[Pengajar, str] = pengajar_model.db.get_pengajar_by_id(pengajar_praktek_id)
            if is_err(pengajar_praktek_res):
                return False, pengajar_praktek_res.unwrap_err()
            pengajar_praktek: Pengajar = pengajar_praktek_res.unwrap()
            new_matkul['praktek']['pengampu'] = pengajar_praktek

        for jenis, komponen in new_matkul.items():
            if jenis == "praktek" and komponen['nama'] == "":
                continue

            matkul = MataKuliah(
                id=None,
                nama=komponen['nama'], # pyright: ignore[reportArgumentType]
                tipe=jenis,
                sks=komponen['bobot'], # pyright: ignore[reportArgumentType]
                semester=semester,
                kelas=kelas,
                pengampu=komponen['pengampu'] # pyright: ignore[reportArgumentType]
            )

            success, message = self.addMataKuliahToDatabase(matkul)
            if not success:
                return success, message

            self.addMataKuliahToList(matkul)

        return True, "Mata kuliah baru berhasil ditambahkan"

    @Slot(str, str, int, int, int, str, str, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def add(
        self,
        nama: str,
        tipe: str,
        sks: int,
        semester: int,
        kelas: int,
        pengajar_teori_id: str,
        pengajar_praktek_id: str,
    ) -> dict[str, bool | str]:
        """Menambahkan mata kuliah baru ke model dan database."""
        success, message = self.fnAdd(nama, tipe, sks, semester, kelas, pengajar_teori_id, pengajar_praktek_id)
        return {"success": success, "message": message}

    def fnUpdate(
        self, id: int, nama: str, semester: int, kelas: int, pengampu_id: str
    ) -> tuple[bool, str]:
        """Method untuk mengubah data mata kuliah yang ada di model."""
        success: bool = False
        message: str = "Gagal memperbarui data mata kuliah"

        # filtered_data: list[Pengajar] = []
        for index, matkul in enumerate[MataKuliah](self._all_data):
            if matkul.getId() != id:
                continue

            pengampu_res: Result[Pengajar, str] = PengajarModel(self.db).db.get_pengajar_by_id(pengampu_id)
            if is_err(pengampu_res):
                return False, pengampu_res.unwrap_err()
            pengampu: Pengajar = pengampu_res.unwrap()

            res: Result[str, str] = self.db.update_matakuliah(
                id=id,
                matkul=MataKuliah(
                    id=id,
                    nama=nama,
                    semester=semester,
                    kelas=kelas,
                    pengampu=pengampu
                )
            )
            if is_err(res):
                return False, res.unwrap_err()

            success = True
            message = res.unwrap()

            matkul.setNama(nama)
            matkul.setSemester(semester)
            matkul.setKelas(kelas)
            matkul.setPengampu(pengampu)

            # Beri tahu QML View bahwa data pada index tersebut telah berubah untuk role tertentu
            roles_to_notify: list[int] = [PengajarModel.ID_ROLE, PengajarModel.NAMA_ROLE, PengajarModel.TIPE_ROLE, PengajarModel.WAKTU_ROLE]
            model_index: QModelIndex = self.index(index, 0)
            self.dataChanged.emit(model_index, model_index, roles_to_notify)

            break

        self.fnFilter(self._filter_query, self._filter_tipe)
        return success, message

    @Slot(int, str, int, int, str, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def update(
        self, id: int, nama: str, semester: int, kelas: int, pengampu_id: str
    ) -> dict[str, bool | str]:
        """Memperbarui item berdasarkan ID dan memancarkan sinyal dataChanged."""
        success, message = self.fnUpdate(id, nama, semester, kelas, pengampu_id)
        return {"success": success, "message": message}

    def getIndexById(self, id: int) -> int:
        # for i, item in enumerate(self._all_data):
        for i, item in enumerate[MataKuliah](self._filtered):
            if item.getId() == id:
                return i

        return -1

    def fnGetById(self, id: int) -> MataKuliah | None:
        """Mengambil data mata kuliah berdasarkan id."""
        for matkul in self._all_data:
            if matkul.getId() == id:
                return matkul

        return None

    @Slot(int, result=QObject)  # pyright: ignore[reportAny]
    def getById(self, id: int) -> MataKuliah | None:
        return self.fnGetById(id)

    def fnGetByIndex(self, index: int) -> MataKuliah | None:
        """
        Method untuk mengambil data pengajar berdasarkan index.
        """
        # if 0 <= index < self.rowCount():
        if 0 <= index < len(self._all_data):
            return self._all_data[index]

        return None

    @Slot(int, result=QObject)  # pyright: ignore[reportAny]
    def getByIndex(self, index: int) -> MataKuliah | None:
        return self.fnGetByIndex(index)

    @Slot(int, result=QObject)  # pyright: ignore[reportAny]
    def getFilteredByIndex(self, index: int) -> MataKuliah | None:
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

    def fnRemoveById(self, id: int) -> dict[str, bool | str]:
        """Method untuk menghapus mata kuliah berdasarkan id key."""
        index: int = self.getIndexById(id)

        self.beginRemoveRows(QModelIndex(), index, index)
        res: Result[str, str] = self.db.delete_matakuliah(id)
        if is_err(res):
            self.endRemoveRows()
            return {"success": False, "message": res.unwrap_err()}


        del self._all_data[index]
        del self._filtered[index]
        self.endRemoveRows()

        return {"success": True, "message": res.unwrap()}

    @Slot(int, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def removeById(self, id: int) -> dict[str, bool | str]:
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
        def cocok(p: MataKuliah):
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
        semua_matkul: list[MataKuliah] = self.db.get_all_matakuliah()
        for matkul in semua_matkul:
            self.addMataKuliahToList(matkul)

    @Slot()  # pyright: ignore[reportAny]
    def reload(self) -> None:
        # self.beginResetModel()
        self._all_data.clear()
        self._filtered.clear()
        # self.endResetModel()
        self.loadDatabase()
