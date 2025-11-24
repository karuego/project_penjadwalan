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

from utils import (  # pyright: ignore[reportImplicitRelativeImport]
    TimeSlot,
    Database,
    TimeSlotManager,
)


class WaktuModel(QAbstractListModel):
    # Definisikan roles untuk setiap properti data
    ID_ROLE: int = int(Qt.ItemDataRole.UserRole) + 1
    HARI_ROLE: int = int(Qt.ItemDataRole.UserRole) + 2
    MULAI_ROLE: int = int(Qt.ItemDataRole.UserRole) + 3
    SELESAI_ROLE: int = int(Qt.ItemDataRole.UserRole) + 4

    def __init__(self, db: Database, parent: QObject | None = None):
        super().__init__(parent)
        self._db: Database = db
        self._timeslot_manager: TimeSlotManager = TimeSlotManager(self._db)
        self._data: list[TimeSlot] = []

    @typing.override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> int | str | datetime | None:
        if not index.isValid():
            return None

        item: TimeSlot = self._data[index.row()]

        return {
            self.ID_ROLE: item.getId(),
            self.HARI_ROLE: item.getHari(),
            self.MULAI_ROLE: item.getMulai(),
            self.SELESAI_ROLE: item.getSelesai(),
        }.get(role, None)

    @typing.override
    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex | None = None,  # pyright: ignore[reportRedeclaration]
    ) -> int:
        """Mengembalikan jumlah total item dalam model."""
        if parent is None:
            parent: QModelIndex = QModelIndex()

        return len(self._data)

    @typing.override
    def roleNames(self) -> dict[int, QByteArray]:
        """Menghubungkan roles dengan nama yang akan digunakan di QML."""
        return {
            self.ID_ROLE: QByteArray(b"id_"),
            self.HARI_ROLE: QByteArray(b"hari"),
            self.MULAI_ROLE: QByteArray(b"mulai"),
            self.SELESAI_ROLE: QByteArray(b"selesai"),
        }

    def addTimeslotToList(self, timeslot: TimeSlot) -> None:
        """Method untuk menambahkan timeslot ke database."""
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(timeslot)
        self.endInsertRows()

    def addTimeslotToDatabase(self, timeslot: TimeSlot) -> tuple[bool, str]:
        """Method untuk menambahkan timeslot ke database."""
        success, timeslot_id, message = self._timeslot_manager.add_timeslot(
            timeslot.getHari(), timeslot.getMulai(), timeslot.getSelesai()
        )
        if success:
            timeslot.setId(typing.cast(int, timeslot_id))

        return success, message

    def loadDatabase(self) -> None:
        all_timeslots: list[TimeSlot] = self._timeslot_manager.get_all_timeslots()
        for timeslot in all_timeslots:
            self.addTimeslotToList(timeslot)

    @Slot()  # pyright: ignore[reportAny]
    def reload(self) -> None:
        self.beginResetModel()
        self._data.clear()
        self.loadDatabase()
        self.endResetModel()

    @Slot(str, str, str)  # pyright: ignore[reportAny]
    def addData(self, hari: int, mulai: str, selesai: str) -> None:
        posisi = 0
        while posisi < len(self._data):
            item: TimeSlot = self._data[posisi]

            # TODO: fix
            # urut berdasarkan: hari, waktu mulai
            if (item.getHari(), item.getMulai()) > (hari, mulai):
                break
            posisi += 1

        new_item = TimeSlot(hari=hari, mulai=mulai, selesai=selesai)
        self.beginInsertRows(QModelIndex(), posisi, posisi)
        self._data.insert(posisi, new_item)
        self.endInsertRows()

    def addTimeslot(self, timeslot: TimeSlot) -> tuple[bool, str]:
        """Method untuk menambahkan timeslot ke database."""
        success = True
        message = "Berhasil"

        if timeslot.getId() <= -1:
            success, message = self.addTimeslotToDatabase(timeslot)

        if success:
            self.addTimeslotToList(timeslot)

        return success, message

    @Slot(int, str, str, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def addWaktu(self, hari: int, mulai: str, selesai: str) -> dict[str, bool | str]:
        """Method untuk menambahkan waktu baru."""
        timeslot: TimeSlot = TimeSlot(
            hari=hari,
            mulai=mulai,
            selesai=selesai,
        )

        success, message = self.addTimeslot(timeslot)
        return {"success": success, "message": message}

    def fnGetIndex(self, index: int) -> TimeSlot | None:
        if 0 <= index < len(self._data):
            return self._data[index]
        return None

    @Slot()  # pyright: ignore[reportAny]
    def getIndex(self, index: int) -> TimeSlot | None:
        return self.fnGetIndex(index)

    def fnGetId(self, id: int) -> TimeSlot | None:
        """
        Method untuk mengambil data pengajar berdasarkan id.
        """
        for item in self._data:
            if int(item.getId()) == int(id):
                print(item.id)
                return item

        return None

    @Slot(int, result=QObject)  # pyright: ignore[reportAny]
    def getId(self, id: int) -> TimeSlot | None:
        return self.fnGetId(id)

    def getIndexById(self, id: int) -> int:
        for i, item in enumerate(self._data):
            if int(item.getId()) == int(id):
                return i

        return -1

    def fnRemoveIndex(self, index: int) -> None:
        """Method untuk menghapus pengajar berdasarkan index dari pada ListView QML."""
        if 0 <= index < self.rowCount():
            self.beginRemoveRows(QModelIndex(), index, index)
            del self._data[index]
            print(index)
            self.endRemoveRows()

    @Slot(int)  # pyright: ignore[reportAny]
    def removeIndex(self, index: int) -> None:
        self.fnRemoveIndex(index)

    def fnRemoveId(self, id: int) -> None:
        """Method untuk menghapus waktu berdasarkan id."""
        index: int = self.getIndexById(id)

        self.beginRemoveRows(QModelIndex(), index, index)
        success, _ = self._timeslot_manager.delete_timeslot(id)
        if not success:
            # TODO: tampilkan pesan ke alertDialog di QML
            return

        del self._data[index]
        self.endRemoveRows()

    @Slot(int)  # pyright: ignore[reportAny]
    def removeId(self, id: int) -> None:
        self.fnRemoveId(id)
