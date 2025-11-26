from PySide6.QtCore import (
    Property,
    QObject,
    QSortFilterProxyModel,
    Qt,
    Signal,
    Slot,
)
from myapp.model import (
    MataKuliahModel,
    PengajarModel,
    PengajarProxyModel,
    RuanganModel,
    WaktuModel,
    WaktuProxyModel,
)
from myapp.utils import (
    Database,
    Hari,
    Pengajar,
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

        self.loadDatabase()

    @Property(QObject, constant=True)
    def waktuModel(self) -> WaktuModel:
        return self._waktu_model

    @Property(QObject, constant=True)
    def waktuProxy(self) -> QSortFilterProxyModel:
        return self._waktu_proxy

    @Property(QObject, constant=True)
    def pengajarModel(self) -> PengajarModel:
        """Model asli yang berisi semua data pengajar."""
        return self._pengajar_model

    @Property(QObject, constant=True)
    def pengajarProxy(self) -> QSortFilterProxyModel:
        """Proxy model yang akan digunakan oleh ListView untuk filtering."""
        return self._pengajar_proxy

    @Property(QObject, constant=True)
    def matakuliahModel(self) -> MataKuliahModel:
        return self._matakuliah_model

    @Property(QObject, constant=True)
    def ruanganModel(self) -> RuanganModel:
        return self._ruangan_model

    @Property(list, constant=True, final=True)
    def namaNamaHari(self) -> list[str]:
        return Hari.getAll()

    @Property(list, constant=True, final=True)
    def namaNamaHariId(self) -> list[int]:
        return Hari.getAllId()

    @Property(list, constant=True, final=True)
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

    def loadPengajar(self):
        data_pengajar: list[Pengajar] = [
            Pengajar(
                id="123000001", nama="Dr. Budi Santoso", tipe="dosen", waktu="1,2"
            ),
            Pengajar(id="21650001", nama="Asisten 1", tipe="asdos", waktu="3,4"),
            Pengajar(
                id="123000002", nama="Prof. Ika Wijayanti", tipe="dosen", waktu="2,3"
            ),
            Pengajar(id="21650002", nama="Asisten 2", tipe="asdos", waktu="3,5"),
            Pengajar(id="21650003", nama="Asisten 3", tipe="asdos", waktu="1,5"),
            Pengajar(
                id="123000003", nama="Ahmad Abdullah, M.Kom", tipe="dosen", waktu=""
            ),
            Pengajar(id="21650004", nama="Asisten 4", tipe="asdos", waktu="1,2"),
            Pengajar(id="21650005", nama="Asisten 5", tipe="asdos", waktu="4,6"),
            Pengajar(id="21650006", nama="Asisten 6", tipe="asdos", waktu=""),
        ]

        # Inisialisasi model pengajar
        self._pengajar_model.setDataPengajar(data_pengajar)

        # Menambahkan beberapa data pengajar
        # pengajar_model.addPengajar("Dr. Budi Santoso", "Dosen", "1,2")
        # pengajar_model.addPengajar("Prof. Ika Wijayanti", "Dosen", "2,3")
        # pengajar_model.addPengajar("Ahmad Abdullah, M.Kom", "Dosen", "")
        # pengajar_model.addPengajar("Asisten 1", "Asdos", "3,4")
        # pengajar_model.addPengajar("Asisten 2", "Asdos", "3,5")

    # TODO: hapus yng tdk diperlukan
    @Slot(str)  # pyright: ignore[reportAny]
    def filterPengajar(self, text: str) -> None:
        """Slot untuk mengatur filter teks pada proxy model."""
        self._pengajar_proxy.setFilterFixedString(text)

    @Slot(int)  # pyright: ignore[reportAny]
    def removePengajarFromIndex(self, proxy_row: int) -> None:
        """Menghapus pengajar dengan aman menggunakan indeks dari proxy model."""
        if 0 <= proxy_row < self._pengajar_proxy.rowCount():
            proxy_index = self._pengajar_proxy.index(proxy_row, 0)
            source_index = self._pengajar_proxy.mapToSource(proxy_index)
            self._pengajar_model.removeByIndex(source_index.row())  # pyright: ignore[reportAny]

    # Gunakan QVariant agar QML bisa menerima dictionary
    @Slot(int, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def getPengajarFromProxyIndex(self, proxy_row: int):
        """Mengambil data pengajar dengan aman menggunakan indexks dari proxy model."""
        if 0 <= proxy_row < self._pengajar_proxy.rowCount():
            proxy_index = self._pengajar_proxy.index(proxy_row, 0)
            source_index = self._pengajar_proxy.mapToSource(proxy_index)
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
