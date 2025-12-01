from PySide6.QtCore import (
    Property,
    QObject,
    QSortFilterProxyModel,
    Qt,
    Signal,
)
from myapp.model import (
    MataKuliahModel,
    PengajarModel,
    PengajarProxyModel,
    RuanganModel,
    WaktuModel,
    WaktuProxyModel,
    JadwalModel,
)
from myapp.utils import (
    Database,
    Hari,
)


class ContextBridge(QObject):
    counterChanged: Signal = Signal()

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._counter: int = 0

        self._db: Database = Database()

        self._waktu_model: WaktuModel = WaktuModel(self._db)
        self._pengajar_model: PengajarModel = PengajarModel(self._db)
        self._matakuliah_model: MataKuliahModel = MataKuliahModel(self._db)
        self._ruangan_model: RuanganModel = RuanganModel(self._db)

        # Inisialisasi proxy model
        self._waktu_proxy: QSortFilterProxyModel = QSortFilterProxyModel()
        self._waktu_proxy.setSourceModel(self._waktu_model)
        self._waktu_proxy.setSortRole(WaktuModel.HARI_ROLE)
        self._waktu_proxy.sort(0, Qt.SortOrder.DescendingOrder)
        self._waktu_proxy2: WaktuProxyModel = WaktuProxyModel(self._waktu_model)

        self._pengajar_proxy: QSortFilterProxyModel = QSortFilterProxyModel()
        self._pengajar_proxy.setSourceModel(self._pengajar_model)
        self._pengajar_proxy.setFilterRole(PengajarModel.TIPE_ROLE)
        self._pengajar_proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownMemberType]

        self._pengajar_proxy2: PengajarProxyModel = PengajarProxyModel(
            self._pengajar_model
        )

        self._jadwal_model: JadwalModel = JadwalModel(self._db)

        self.loadDatabase()

    @Property(QObject, constant=True)  # pyright: ignore[reportCallIssue]
    def waktuModel(self) -> WaktuModel:
        return self._waktu_model

    @Property(QObject, constant=True)  # pyright: ignore[reportCallIssue]
    def waktuProxy(self) -> QSortFilterProxyModel:
        return self._waktu_proxy

    @Property(QObject, constant=True)  # pyright: ignore[reportCallIssue]
    def pengajarModel(self) -> PengajarModel:
        """Model asli yang berisi semua data pengajar."""
        return self._pengajar_model

    @Property(QObject, constant=True)  # pyright: ignore[reportCallIssue]
    def pengajarProxy(self) -> QSortFilterProxyModel:
        """Proxy model yang akan digunakan oleh ListView untuk filtering."""
        return self._pengajar_proxy

    @Property(QObject, constant=True)  # pyright: ignore[reportCallIssue]
    def matakuliahModel(self) -> MataKuliahModel:
        return self._matakuliah_model

    @Property(QObject, constant=True)  # pyright: ignore[reportCallIssue]
    def ruanganModel(self) -> RuanganModel:
        return self._ruangan_model

    @Property(QObject, constant=True)  # pyright: ignore[reportCallIssue]
    def jadwalModel(self) -> JadwalModel:
        return self._jadwal_model

    @Property(list, constant=True)  # pyright: ignore[reportCallIssue]
    def namaNamaHari(self) -> list[str]:
        return Hari.getAll()

    @Property(list, constant=True)  # pyright: ignore[reportCallIssue]
    def namaNamaHariId(self) -> list[int]:
        return Hari.getAllId()

    @Property(list, constant=True)  # pyright: ignore[reportCallIssue]
    def namaNamaHariDict(self) -> list[dict[str, str | int]]:
        allDays: list[dict[str, str | int]] = []
        for idx, hari in enumerate(Hari.getAll()):
            allDays.append({"idx": idx + 1, "hari": hari})
        return allDays

    def loadDatabase(self) -> None:
        self._waktu_model.loadDatabase()
        self._pengajar_model.loadDatabase()
        # self.loadPengajar()
        self._matakuliah_model.loadDatabase()
        self._ruangan_model.loadDatabase()
        self._jadwal_model.loadDatabase()

    def getCounter(self) -> int:
        return self._counter

    def setCounter(self, value: int) -> None:
        if self._counter != value:
            self._counter = value
            self.counterChanged.emit()

    counter: Property = Property(int, getCounter, setCounter, None, "")
