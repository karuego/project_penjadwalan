import typing
from PySide6.QtCore import Qt, Slot, QByteArray, QObject
from PySide6.QtCore import QAbstractListModel, QModelIndex, QPersistentModelIndex

from utils import Database  # pyright: ignore[reportImplicitRelativeImport]


class MataKuliahModel(QAbstractListModel):
    # Definisikan "roles". Ini adalah nama-nama property yang akan diakses di QML.
    # Misalnya, di QML kita akan memanggil `model.nama` dan `model.deskripsi`
    NAMA_ROLE: int = int(Qt.ItemDataRole.UserRole) + 1
    DESKRIPSI_ROLE: int = int(Qt.ItemDataRole.UserRole) + 2

    def __init__(self, db: Database, parent: QObject | None = None):
        super().__init__(parent)
        self.db: Database = db

        # _data akan menyimpan daftar pengajar. Setiap item adalah dictionary.
        self._data: list[dict[str, str]] = []

    @typing.override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        """Mengembalikan data untuk item dan role tertentu."""
        # beri tahu type checker bahwa kita perlakukan index sebagai QModelIndex
        idx = typing.cast(QModelIndex, index)

        if not idx.isValid():
            return None

        item: dict[str, str] = self._data[idx.row()]

        if role == self.NAMA_ROLE:
            return item["nama"]
        if role == self.DESKRIPSI_ROLE:
            return item["deskripsi"]
        return None

    @typing.override
    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex | None = None,
    ) -> int:
        """Mengembalikan jumlah total item dalam model."""
        if parent is None:
            parent = QModelIndex()

        return len(self._data)

    @typing.override
    def roleNames(self) -> dict[int, QByteArray]:
        """Menghubungkan roles dengan nama yang akan digunakan di QML."""
        return {
            self.NAMA_ROLE: QByteArray(b"nama"),
            self.DESKRIPSI_ROLE: QByteArray(b"deskripsi"),
        }

    @Slot(str, str)  # pyright: ignore[reportAny]
    def addPengajar(self, nama: str, deskripsi: str) -> None:
        """Method untuk menambahkan pengajar baru ke model."""
        # Memberi tahu view bahwa kita akan menambahkan barus baru
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())

        # Tambahkan data baru ke list internal
        self._data.append({"nama": nama, "deskripsi": deskripsi})

        # Memberi tahu view bahwa penambahan baris telah selesai
        self.endInsertRows()

    @Slot(int)  # pyright: ignore[reportAny]
    def removePengajar(self, index: int):
        """Method untuk menghapus pengajar berdasarkan index."""
        # Pastikan index valid
        if 0 <= index < self.rowCount():
            # Memberi tahu view bahwa kita akan menghapus baris
            self.beginRemoveRows(QModelIndex(), index, index)

            # Hapus data dari list internal
            del self._data[index]

            # Memberi tahu view bahwa penghapusan baris telah selesai
            self.endRemoveRows()
