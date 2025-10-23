from utils import Database  # pyright: ignore[reportImplicitRelativeImport]

import typing
from PySide6.QtCore import (
    Qt,
    QByteArray,
    QObject,
    QAbstractListModel,
    QModelIndex,
    QPersistentModelIndex,
)
from utils import Ruangan  # pyright: ignore[reportImplicitRelativeImport]


class RuanganModel(QAbstractListModel):
    ID_ROLE: int = int(Qt.ItemDataRole.UserRole) + 1
    NAMA_ROLE: int = int(Qt.ItemDataRole.UserRole) + 2
    TIPE_ROLE: int = int(Qt.ItemDataRole.UserRole) + 3

    def __init__(self, db: Database, parent: QObject | None = None):
        super().__init__(parent)
        self._data: list[Ruangan] = []

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

        item: Ruangan = self._data[idx.row()]
        # item: Ruangan = self._filtered[idx.row()]

        if role == self.ID_ROLE:
            return item.getId()
        if role == self.NAMA_ROLE:
            return item.getNama()
        if role == self.TIPE_ROLE:
            return item.getTipe()
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

        return len(self._data)
        # return len(self._filtered)

    @typing.override
    def roleNames(self) -> dict[int, QByteArray]:
        """
        Menghubungkan roles dengan nama yang akan digunakan di QML.
        """
        return {
            self.ID_ROLE: QByteArray(b"id_"),
            self.NAMA_ROLE: QByteArray(b"nama"),
            self.TIPE_ROLE: QByteArray(b"tipe"),
        }
