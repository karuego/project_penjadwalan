from myapp.utils.worker_scheduler import OptimizationWorker
import sqlite3
import typing
from result import Result, Ok, Err, is_ok, is_err
from maybe import Maybe, Some, Nothing

from PySide6.QtCore import (
    QAbstractTableModel,
    QByteArray,
    QModelIndex,
    QObject,
    QPersistentModelIndex,
    Qt,
    Slot,
    QThread,
)
from myapp import log
from myapp.utils import Database
from myapp.utils import sa as v6
from myapp.utils.struct_jadwal import Jadwal
from myapp.utils.struct_matakuliah import MataKuliah
from myapp.utils.worker_scheduler import OptimizationWorker


class JadwalModel(QAbstractTableModel):
    ID_ROLE: int = int(Qt.ItemDataRole.UserRole) + 1
    HARI_ROLE: int = int(Qt.ItemDataRole.UserRole) + 2
    JAM_ROLE: int = int(Qt.ItemDataRole.UserRole) + 3
    MATAKULIAH_ROLE: int = int(Qt.ItemDataRole.UserRole) + 4
    TIPE_ROLE: int = int(Qt.ItemDataRole.UserRole) + 5
    SKS_ROLE: int = int(Qt.ItemDataRole.UserRole) + 6
    SEMESTER_ROLE: int = int(Qt.ItemDataRole.UserRole) + 7
    KELAS_ROLE: int = int(Qt.ItemDataRole.UserRole) + 8
    RUANGAN_ROLE: int = int(Qt.ItemDataRole.UserRole) + 9
    DARING_ROLE: int = int(Qt.ItemDataRole.UserRole) + 10
    PENGAJAR_ROLE: int = int(Qt.ItemDataRole.UserRole) + 11

    _filter_query: str = ""  # pyright: ignore[reportRedeclaration]
    _filter_tipe: str = "teori"  # pyright: ignore[reportRedeclaration]

    def __init__(self, db: Database, parent: QObject | None = None):
        super().__init__(parent)
        self.db: Database = db
        self._data: list[Jadwal] = []
        self._filtered: list[Jadwal] = []

        # Definisi nama kolom header
        self._headers: list[str] = [
            "ID",
            "Hari",
            "Jam",
            "Mata Kuliah",
            "Jenis",
            "SKS",
            "Semester",
            "Kelas",
            "Ruangan",
            "Daring",
            "Nama Pengajar",
        ]

    @typing.override
    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex | None = None
    ) -> int:
        """Menentukan Jumlah Baris"""
        if parent is None:
            parent = QModelIndex()

        # return len(self._all_data)
        return len(self._filtered)

    @typing.override
    def columnCount(
        self, parent: QModelIndex | QPersistentModelIndex | None = None
    ) -> int:
        """Menentukan Jumlah Kolom"""
        if parent is None:
            parent = QModelIndex()
        return len(self._headers)

    @typing.override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> int | str | bool | None:
        """Mengambil Data untuk setiap Sel (Baris x Kolom)."""
        if not index.isValid():
            return None

        # Kita hanya melayani DisplayRole (untuk teks di layar)
        if role == Qt.ItemDataRole.DisplayRole:
            return None

        row: int = index.row()
        col: int = index.column()

        # Ambil object/dictionary dari list
        item: Jadwal = self._data[row]

        return {
            0: item.getId(),
            1: item.getHari(),
            2: item.getJam(),
            3: item.getMatakuliah(),
            4: item.getJenis(),
            5: item.getSks(),
            6: item.getSemester(),
            7: item.getKelas(),
            8: item.getRuangan(),
            9: item.getDaring(),
            10: item.getPengajar(),
        }.get(col, None)

    @typing.override
    def roleNames(self) -> dict[int, QByteArray]:
        """Menghubungkan roles dengan nama yang akan digunakan di QML."""
        return {
            Qt.ItemDataRole.DisplayRole: QByteArray(b"display"),
            self.ID_ROLE: QByteArray(b"id_"),
            self.HARI_ROLE: QByteArray(b"hari"),
            self.JAM_ROLE: QByteArray(b"jam"),
            self.MATAKULIAH_ROLE: QByteArray(b"matakuliah"),
            self.TIPE_ROLE: QByteArray(b"tipe"),
            self.SKS_ROLE: QByteArray(b"sks"),
            self.SEMESTER_ROLE: QByteArray(b"semester"),
            self.KELAS_ROLE: QByteArray(b"kelas"),
            self.RUANGAN_ROLE: QByteArray(b"ruangan"),
            self.DARING_ROLE: QByteArray(b"daring"),
            self.PENGAJAR_ROLE: QByteArray(b"pengajar"),
        }

    @typing.override
    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        """Mengatur Header (Judul Kolom)"""
        # section = nomor kolom (0, 1, 2...) jika orientation horizontal
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if 0 <= section < len(self._headers):
                    return self._headers[section]
        return None

    def setDataJadwal(self, data: list[Jadwal]) -> None:
        self._data = list[Jadwal](data)
        self._filtered = list[Jadwal](data)

    def addToList(self, jadwal: Jadwal) -> None:
        """Method untuk menambahkan jadwal ke database."""
        self._data.append(jadwal)
        self._filtered.append(jadwal)
        self.fnFilter(self._filter_query, self._filter_tipe)

    def addToDatabase(self, jadwal: Jadwal) -> Result[str, str]:
        """Menambahkan jadwal baru ke database"""
        conn = self.db.get_connection()
        cursor: sqlite3.Cursor = conn.cursor()
        _ = cursor.execute("PRAGMA foreign_keys = ON;")

        try:
            _ = cursor.execute(
                """
                    INSERT INTO jadwal (nama, jenis, sks, semester, jumlah_kelas, pengajar_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    jadwal.getNama(),
                    jadwal.getTipe(),
                    jadwal.getSks(),
                    jadwal.getSemester(),
                    jadwal.getKelas(),
                    jadwal.getPengampu().getId(),  # pyright: ignore[reportOptionalMemberAccess]
                ),
            )

            jadwal_id_baru: int | None = cursor.lastrowid
            if not jadwal_id_baru:
                log.info("Gagal menambahkan mata kuliah")
                return False, "Gagal menambahkan mata Kuliah"

            log.info(
                f"Mata Kuliah '{jadwal.getNama()}' dibuat dengan ID: {jadwal_id_baru}"
            )
            jadwal.setId(jadwal_id_baru)

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
        pengajar_teori_res: Result[Pengajar, str] = (
            pengajar_model.db.get_pengajar_by_id(pengajar_teori_id)
        )
        if is_err(pengajar_teori_res):
            return False, pengajar_teori_res.unwrap_err()
        pengajar_teori: Pengajar = pengajar_teori_res.unwrap()

        new_matkul: dict[str, dict[str, str | int | Pengajar]] = {
            "teori": {"nama": nama.strip(), "bobot": sks, "pengampu": pengajar_teori},
            "praktek": {"nama": "", "bobot": 0, "pengampu": Pengajar()},
        }

        if tipe == "praktek":
            new_matkul["teori"]["bobot"] = new_matkul["teori"]["bobot"] - 1  # pyright: ignore[reportOperatorIssue]
            new_matkul["praktek"]["nama"] = f"Praktikum {nama.strip()}"
            new_matkul["praktek"]["bobot"] = 1

            pengajar_praktek_res: Result[Pengajar, str] = (
                pengajar_model.db.get_pengajar_by_id(pengajar_praktek_id)
            )
            if is_err(pengajar_praktek_res):
                return False, pengajar_praktek_res.unwrap_err()
            pengajar_praktek: Pengajar = pengajar_praktek_res.unwrap()
            new_matkul["praktek"]["pengampu"] = pengajar_praktek

        for jenis, komponen in new_matkul.items():
            if jenis == "praktek" and komponen["nama"] == "":
                continue

            matkul = MataKuliah(
                id=None,
                nama=komponen["nama"],  # pyright: ignore[reportArgumentType]
                tipe=jenis,
                sks=komponen["bobot"],  # pyright: ignore[reportArgumentType]
                semester=semester,
                kelas=kelas,
                pengampu=komponen["pengampu"],  # pyright: ignore[reportArgumentType]
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
        success, message = self.fnAdd(
            nama, tipe, sks, semester, kelas, pengajar_teori_id, pengajar_praktek_id
        )
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

            pengampu_res: Result[Pengajar, str] = PengajarModel(
                self.db
            ).db.get_pengajar_by_id(pengampu_id)
            if is_err(pengampu_res):
                return False, pengampu_res.unwrap_err()
            pengampu: Pengajar = pengampu_res.unwrap()

            res: Result[str, str] = self.db.update_matakuliah(
                id=id,
                matkul=MataKuliah(
                    id=id, nama=nama, semester=semester, kelas=kelas, pengampu=pengampu
                ),
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
            roles_to_notify: list[int] = [
                PengajarModel.ID_ROLE,
                PengajarModel.NAMA_ROLE,
                PengajarModel.TIPE_ROLE,
                PengajarModel.WAKTU_ROLE,
            ]
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
        semua_jadwal: list[Jadwal] = self.db.get_all_jadwal()
        for jadwal in semua_jadwal:
            self.addToList(jadwal)

    def fnReload(self) -> None:
        self.beginResetModel()
        self._data.clear()
        self._filtered.clear()
        self.endResetModel()

        self.loadDatabase()

    @Slot()  # pyright: ignore[reportAny]
    def reload(self) -> None:
        self.fnReload()
