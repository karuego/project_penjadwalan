import typing
from datetime import datetime

from PySide6.QtCore import (
    Qt,
    Slot,
    QByteArray,
    QObject,
)
from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QPersistentModelIndex,
)

from utils import Hari, TimeSlot, Database  # pyright: ignore[reportImplicitRelativeImport]


class WaktuModel(QAbstractListModel):
    # Definisikan roles untuk setiap properti data
    ID_ROLE: int = int(Qt.ItemDataRole.UserRole) + 1
    HARI_ROLE: int = int(Qt.ItemDataRole.UserRole) + 2
    MULAI_ROLE: int = int(Qt.ItemDataRole.UserRole) + 3
    SELESAI_ROLE: int = int(Qt.ItemDataRole.UserRole) + 4
    CREATED_AT_ROLE: int = int(Qt.ItemDataRole.UserRole) + 5

    def __init__(self, db: Database, parent: QObject | None = None):
        super().__init__(parent)
        # self._data: list[dict[str, str]] = []
        self._data: list[TimeSlot] = []
        self.db: Database = db

    @typing.override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> int | str | datetime | None:
        idx = index
        if not idx.isValid():
            return None

        # item: dict[str, str] = self._data[idx.row()]
        item: TimeSlot = self._data[idx.row()]

        return {
            self.ID_ROLE: item.getId(),
            self.HARI_ROLE: Hari.getNama(item.getHari() or 0),
            self.MULAI_ROLE: item.getMulai(),
            self.SELESAI_ROLE: item.getSelesai(),
            self.CREATED_AT_ROLE: item.getCreatedAt(),
        }.get(role, None)

    @typing.override
    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex | None = None
    ) -> int:
        """Mengembalikan jumlah total item dalam model."""
        if parent is None:
            parent = QModelIndex()

        return len(self._data)

    @typing.override
    def roleNames(self) -> dict[int, QByteArray]:
        """Menghubungkan roles dengan nama yang akan digunakan di QML."""
        return {
            self.ID_ROLE: QByteArray(b"id_"),
            self.HARI_ROLE: QByteArray(b"hari"),
            self.MULAI_ROLE: QByteArray(b"mulai"),
            self.SELESAI_ROLE: QByteArray(b"selesai"),
            self.CREATED_AT_ROLE: QByteArray(b"createdAt"),
        }

    @Slot(str, str, str)  # pyright: ignore[reportAny]
    def addWaktu(self, hari: int, mulai: str, selesai: str) -> None:
        """Method untuk menambahkan waktu baru dari QML."""
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        # self._data.append(
        #     {
        #         "hari": hari,
        #         "mulai": mulai,
        #         "selesai": selesai,
        #     }
        # )

        # TODO: urus `id` dan `created_at`
        self._data.append(
            TimeSlot(-1, hari, mulai, selesai, datetime.now().isoformat())
        )
        self.endInsertRows()

    @Slot(str, str, str)  # pyright: ignore[reportAny]
    def addTimeSlot(self, timeslot: TimeSlot) -> None:
        """Method untuk menambahkan waktu baru dari QML."""
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(timeslot)
        self.endInsertRows()

    def getIndexById(self, id: int) -> int:
        for i, item in enumerate(self._data):
            if int(item.getId()) == int(id):
                return i

        return -1

    @Slot(int, result=QObject)  # pyright: ignore[reportAny]
    def getById(self, id: int) -> TimeSlot | None:
        """
        Method untuk mengambil data pengajar berdasarkan id.
        """
        for item in self._data:
            if int(item.getId()) == int(id):
                print(item.id)
                return item

        print("None")
        return None

    # @Slot(int, result="QVariantMap")
    # def getByIndex(self, index: int) -> dict[str, str]:
    #     """
    #     Method untuk mengambil data pengajar berdasarkan index.
    #     """
    #     # if 0 <= index < self.rowCount():
    #     if 0 <= index < len(self._data):
    #         return self._data[index]

    #     return {}

    @Slot(int)  # pyright: ignore[reportAny]
    def removeWaktuByIndex(self, index: int):
        """Method untuk menghapus pengajar berdasarkan index dari QML."""
        if 0 <= index < self.rowCount():
            self.beginRemoveRows(QModelIndex(), index, index)
            del self._data[index]
            print(index)
            self.endRemoveRows()

    @Slot(int)  # pyright: ignore[reportAny]
    def removeWaktuById(self, id: int):
        """Method untuk menghapus pengajar berdasarkan id dari QML."""
        if id <= 0:
            return

        index = self.getIndexById(id)

        self.beginRemoveRows(QModelIndex(), index, index)
        success, message = self.db.timeslot_manager.delete_timeslot(id)
        print(success)
        print(message)

        del self._data[index]
        self.endRemoveRows()
