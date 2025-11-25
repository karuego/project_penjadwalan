import re
from result.result import Result
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
from utils.database import Database # pyright: ignore[reportImplicitRelativeImport]
from utils.struct_pengajar import Pengajar # pyright: ignore[reportImplicitRelativeImport]


class PengajarModel(QAbstractListModel):
    ID_ROLE: int = int(Qt.ItemDataRole.UserRole) + 1
    NAMA_ROLE: int = int(Qt.ItemDataRole.UserRole) + 2
    TIPE_ROLE: int = int(Qt.ItemDataRole.UserRole) + 3
    WAKTU_ROLE: int = int(Qt.ItemDataRole.UserRole) + 4

    _filter_query: str = ""     # pyright: ignore[reportRedeclaration]
    _filter_tipe: str = "semua" # pyright: ignore[reportRedeclaration]

    def __init__(self, db: Database, parent: QObject | None = None):
        super().__init__(parent)
        self.db: Database = db
        self._all_data: list[Pengajar] = []
        self._filtered: list[Pengajar] = []

    @typing.override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        """Mengembalikan data untuk item dan role tertentu."""

        if not index.isValid():
            return None

        item: Pengajar = self._filtered[index.row()]

        return {
            self.ID_ROLE: item.getId(),
            self.NAMA_ROLE: item.getNama(),
            self.TIPE_ROLE: item.getTipe(),
            self.WAKTU_ROLE: item.getWaktu(),
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
            self.ID_ROLE: QByteArray(b"id_"),
            self.NAMA_ROLE: QByteArray(b"nama"),
            self.TIPE_ROLE: QByteArray(b"tipe"),
            self.WAKTU_ROLE: QByteArray(b"waktu"),
        }

    def setDataPengajar(self, data: list[Pengajar]) -> None:
        self._all_data = list(data)
        self._filtered = list(data)

    def addPengajarToList(self, pengajar: Pengajar) -> None:
        """Method untuk menambahkan pengajar ke database."""
        self._all_data.append(pengajar)
        self._filtered.append(pengajar)
        self.fnFilter(self._filter_query, self._filter_tipe)

    def addPengajarToDatabase(self, pengajar: Pengajar) -> tuple[bool, str]:
        """
        Menambahkan pengajar baru ke database dengan validasi
        Returns: (success, message)
        """
        try:
            # Validasi input
            if not all([pengajar.getId(), pengajar.getNama(), pengajar.getTipe()]):
                return False, "Field id, nama, dan jenis harus diisi"

            # Cek if already exists
            with self.db.get_connection() as conn:
                cursor = conn.cursor()

                query = "SELECT jenis FROM pengajar WHERE id = ?"
                params: list[str] = [pengajar.getId()]
                idn: str = "NIDN" if pengajar.getTipe().lower() == "dosen" else "NIM"

                _ = cursor.execute(query, params)
                data_lama: str | None = cursor.fetchone() # pyright: ignore[reportAny]

                if data_lama is None:
                    _ = cursor.execute(
                        """
                            INSERT INTO pengajar (id, nama, jenis, preferensi_waktu)
                            VALUES (?, ?, ?, ?)
                        """,
                        (pengajar.getId(), pengajar.getNama(), pengajar.getTipe(), pengajar.getWaktu()),
                    )
                    conn.commit()
                    return True, "Pengajar berhasil ditambahkan"
                else:
                    return False, f"Pengajar dengan {idn} {pengajar.getId()} sudah ada"
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def fnAdd(self, id: str, nama: str, tipe: str, waktu: str) -> tuple[bool, str]:
        """Method untuk menambahkan pengajar baru ke model."""
        success = True
        message = "Berhasil"

        pengajar = Pengajar(
            id.strip(),
            nama.strip(),
            tipe.strip(),
            waktu.strip()
        )

        success, message = self.addPengajarToDatabase(pengajar)
        if not success:
            return success, message

        self.addPengajarToList(pengajar)
        return success, message

    @Slot(str, str, str, str, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def add(self, id: str, nama: str, tipe: str, waktu: str) -> dict[str, bool | str]:
        success, message = self.fnAdd(id, nama, tipe, waktu)
        return {"success": success, "message": message}

    def fnUpdate(
        self, old_id: str, new_id: str, nama: str, tipe: str, waktu: str
    ) -> tuple[bool, str]:
        """Method untuk mengubah data pengajar yang ada di model."""
        success: bool = False
        message: str = "Gagal memperbarui data pengajar"

        # filtered_data: list[Pengajar] = []
        for index, pengajar in enumerate[Pengajar](self._all_data):
            if pengajar.getId() != old_id:
                continue

            res: Result[str, str] = self.db.update_pengajar(old_id, Pengajar(new_id, nama, tipe, waktu))
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
        res: Result[str, str] = self.db.delete_pengajar(id)
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
        semua_pengajar: list[Pengajar] = self.db.get_all_pengajar()
        for pengajar in semua_pengajar:
            self.addPengajarToList(pengajar)

    @Slot()  # pyright: ignore[reportAny]
    def reload(self) -> None:
        # self.beginResetModel()
        self._all_data.clear()
        self._filtered.clear()
        # self.endResetModel()
        self.loadDatabase()
