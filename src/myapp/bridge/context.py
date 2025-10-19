from PySide6.QtCore import Slot, Signal, Property, QObject, QSortFilterProxyModel
from model import (  # pyright: ignore[reportImplicitRelativeImport]
    WaktuModel,
    PengajarModel,
    PengajarProxyModel,
    MataKuliahModel,
)


class ContextBridge(QObject):
    counterChanged: Signal = Signal()

    def __init__(
        self,
        waktu_model: WaktuModel,
        pengajar_model: PengajarModel,
        pengajar_proxy_model: QSortFilterProxyModel,
        matakuliah_model: MataKuliahModel,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self._counter: int = 0

        self._waktu_model: WaktuModel = waktu_model

        self._pengajar_model: PengajarModel = pengajar_model
        self._pengajar_proxy_model: QSortFilterProxyModel = pengajar_proxy_model
        self._pengajar_proxy: PengajarProxyModel = PengajarProxyModel(
            self._pengajar_model
        )

        self._matakuliah_model: MataKuliahModel = matakuliah_model

    @Property(QObject, constant=True)
    def waktuModel(self) -> WaktuModel:
        return self._waktu_model

    @Property(QObject, constant=True)
    def pengajarModel(self) -> PengajarModel:
        """Model asli yang berisi semua data pengajar."""
        return self._pengajar_model

    @Property(QObject, constant=True)
    def pengajarProxy(self) -> QSortFilterProxyModel:
        """Proxy model yang akan digunakan oleh ListView untuk filtering."""
        return self._pengajar_proxy

    @Property(QObject, constant=True)
    def mataKuliahModel(self) -> MataKuliahModel:
        return self._matakuliah_model

    @Slot(str)  # pyright: ignore[reportAny]
    def filterPengajar(self, text: str) -> None:
        """Slot untuk mengatur filter teks pada proxy model."""
        self._pengajar_proxy_model.setFilterFixedString(text)

    @Slot(int)  # pyright: ignore[reportAny]
    def removePengajarFromIndex(self, proxy_row: int) -> None:
        """Menghapus pengajar dengan aman menggunakan indeks dari proxy model."""
        if 0 <= proxy_row < self._pengajar_proxy_model.rowCount():
            proxy_index = self._pengajar_proxy_model.index(proxy_row, 0)
            source_index = self._pengajar_proxy_model.mapToSource(proxy_index)
            self._pengajar_model.removeByIndex(source_index.row())  # pyright: ignore[reportAny]

    # Gunakan QVariant agar QML bisa menerima dictionary
    @Slot(int, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def getPengajarFromProxyIndex(self, proxy_row: int):
        """Mengambil data pengajar dengan aman menggunakan indexks dari proxy model."""
        if 0 <= proxy_row < self._pengajar_proxy_model.rowCount():
            proxy_index = self._pengajar_proxy_model.index(proxy_row, 0)
            source_index = self._pengajar_proxy_model.mapToSource(proxy_index)
            return self._pengajar_model.getFilteredByIndex(source_index.row())  # pyright: ignore[reportAny]

        return None

    @Slot(int, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def getPengajarFromSourceIndex(self, source_row: int):
        """Mengambil data pengajar dengan aman menggunakan indexks dari source model."""
        if 0 <= source_row < self._pengajar_model.rowCount():
            return self._pengajar_model.getById(source_row)  # pyright: ignore[reportAny]

        return None

    def getCounter(self) -> int:
        return self._counter

    def setCounter(self, value: int) -> None:
        if self._counter != value:
            self._counter = value
            self.counterChanged.emit()

    counter: Property = Property(int, getCounter, setCounter)
