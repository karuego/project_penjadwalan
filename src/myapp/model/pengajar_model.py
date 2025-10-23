import re
import typing
from PySide6.QtCore import (
    Qt,
    Slot,
    QByteArray,
    QObject,
    QAbstractListModel,
    QModelIndex,
    QPersistentModelIndex,
)

from utils import Database  # pyright: ignore[reportImplicitRelativeImport]
from utils import Pengajar  # pyright: ignore[reportImplicitRelativeImport]


class PengajarModel(QAbstractListModel):
    ID_ROLE: int = int(Qt.ItemDataRole.UserRole) + 1
    NAMA_ROLE: int = int(Qt.ItemDataRole.UserRole) + 2
    TIPE_ROLE: int = int(Qt.ItemDataRole.UserRole) + 3
    WAKTU_ROLE: int = int(Qt.ItemDataRole.UserRole) + 4

    def __init__(self, db: Database, parent: QObject | None = None):
        super().__init__(parent)
        self.db: Database = db

        self._data: list[Pengajar] = []
        self._filtered: list[Pengajar] = []

    def setDataPengajar(self, data: list[Pengajar]) -> None:
        self._data = data
        self._filtered = list(data)

    @typing.override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        """
        Mengembalikan data untuk item dan role tertentu.
        """
        # beri tahu type checker bahwa kita perlakukan index sebagai QModelIndex
        idx = typing.cast(QModelIndex, index)

        if not idx.isValid():
            return None

        # item: dict[str, str] = self._data[idx.row()]
        item: Pengajar = self._filtered[idx.row()]

        if role == self.ID_ROLE:
            return item.getId()
        if role == self.NAMA_ROLE:
            return item.getNama()
        if role == self.TIPE_ROLE:
            return item.getTipe()
        if role == self.WAKTU_ROLE:
            return item.getWaktu()
        return None

    @typing.override
    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex | None = None,
    ) -> int:
        """
        Mengembalikan jumlah total item dalam model.
        """
        if parent is None:
            parent = QModelIndex()

        # return len(self._data)
        return len(self._filtered)

    @typing.override
    def roleNames(self) -> dict[int, QByteArray]:
        """
        Menghubungkan roles dengan nama yang akan digunakan di QML.
        """
        return {
            self.ID_ROLE: QByteArray(b"id_"),
            self.NAMA_ROLE: QByteArray(b"nama"),
            self.TIPE_ROLE: QByteArray(b"tipe"),
            self.WAKTU_ROLE: QByteArray(b"waktu"),
        }

    @Slot(str, str, str, str)  # pyright: ignore[reportAny]
    def add(self, id: str, nama: str, tipe: str, waktu: str) -> None:
        """
        Method untuk menambahkan pengajar baru ke model.
        """
        # Memberi tahu view bahwa kita akan menambahkan barus baru
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())

        # Tambahkan data baru ke list internal
        # self._data.append({"id": id, "nama": nama, "tipe": tipe, "waktu": waktu})
        self._data.append(Pengajar(id, nama, tipe, waktu))

        # Memberi tahu view bahwa penambahan baris telah selesai
        self.endInsertRows()

    def getIndexById(self, id: str) -> int:
        for i, item in enumerate(self._data):
            if item.getId() == id:
                return i

        return -1

    def fnGetById(self, id: str) -> Pengajar | None:
        """
        Method untuk mengambil data pengajar berdasarkan id.
        """
        for item in self._data:
            if item.getId() == id:
                return item

        return None

    @Slot(str, result=QObject)  # pyright: ignore[reportAny]
    def getById(self, id: str) -> Pengajar | None:
        return self.fnGetById(id)

    def fnGetByIndex(self, index: int) -> Pengajar | None:
        """
        Method untuk mengambil data pengajar berdasarkan index.
        """
        # if 0 <= index < self.rowCount():
        if 0 <= index < len(self._data):
            return self._data[index]

        return None

    @Slot(int, result=QObject)  # pyright: ignore[reportAny]
    def getByIndex(self, index: int) -> Pengajar | None:
        return self.fnGetByIndex(index)

    @Slot(int, result=QObject)  # pyright: ignore[reportAny]
    def getFilteredByIndex(self, index: int) -> Pengajar | None:
        if 0 <= index < self.rowCount():
            return self._filtered[index]

        return None

    @Slot(str)  # pyright: ignore[reportAny]
    def removeById(self, id: str):
        """
        Method untuk menghapus pengajar berdasarkan id key.
        """
        index: int = self.getIndexById(id)
        self.beginRemoveRows(QModelIndex(), index, index)
        del self._data[index]
        self.endRemoveRows()

    def fnRemoveByIndex(self, index: int) -> None:
        """
        Method untuk menghapus pengajar berdasarkan index.
        """
        # Pastikan index valid
        if 0 <= index < self.rowCount():
            # Memberi tahu view bahwa kita akan menghapus baris
            self.beginRemoveRows(QModelIndex(), index, index)

            # Hapus data dari list internal
            del self._data[index]

            # Memberi tahu view bahwa penghapusan baris telah selesai
            self.endRemoveRows()

    @Slot(int)  # pyright: ignore[reportAny]
    def removeByIndex(self, index: int) -> None:
        self.fnRemoveByIndex(index)

    @Slot(str, str)  # pyright: ignore[reportAny]
    def filter(self, query: str, tipe: str):
        """
        Filter data berdasarkan nama dan tipe.
        """

        q: str = query.strip().lower()
        t: str = tipe.strip().lower()

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
        for pengajar in self._data:
            if cocok(pengajar):
                self._filtered.append(pengajar)

        # self._filtered = [
        #     pengajar
        #     for pengajar in self._data
        #     if (q in pengajar.getNama().lower())
        #     and (t == "semua" or pengajar.getTipe().lower() == t)
        # ]

        self.endResetModel()

    @Slot(str, str, str, str, str)  # pyright: ignore[reportAny]
    def update(
        self,
        prev_id: str | None = None,
        id: str | None = None,
        nama: str | None = None,
        tipe: str | None = None,
        waktu: str | None = None,
    ) -> None:
        if prev_id is None:
            return

        for i, pengajar in enumerate(self._data):
            if pengajar.getId() == prev_id:
                if id is not None:
                    pengajar.setId(id)
                if nama is not None:
                    pengajar.setNama(nama)
                if tipe is not None:
                    pengajar.setTipe(tipe)
                if waktu is not None:
                    pengajar.setWaktu(waktu)

                # top = self.index(row, 0)
                # bottom = self.index(row, 0)
                # self.dataChanged.emit(top, bottom, [])

                self.dataChanged.emit(self.index(i), self.index(i))
                break
