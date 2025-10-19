import typing
from PySide6.QtCore import (
    Slot,
    Qt,
    QObject,
    QModelIndex,
    QPersistentModelIndex,
    QSortFilterProxyModel,
)

from . import PengajarModel


class PengajarProxyModel(QSortFilterProxyModel):
    def __init__(self, pengajar_model: PengajarModel, parent: QObject | None = None):
        super().__init__(parent)
        self._filter_text: str = ""
        self._pengajar_model: PengajarModel = pengajar_model

        self.setSourceModel(self._pengajar_model)
        self.setFilterRole(PengajarModel.TIPE_ROLE)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownMemberType]

    @Slot(str)  # pyright: ignore[reportAny]
    def setFilterText(self, text: str):
        self._filter_text = text.lower()
        self.invalidateFilter()

    @typing.override
    def filterAcceptsRow(
        self, source_row: int, source_parent: QModelIndex | QPersistentModelIndex
    ) -> bool:
        model = typing.cast(PengajarModel, self.sourceModel())
        index = model.index(source_row, 0, source_parent)

        nama = model.data(index, PengajarModel.NAMA_ROLE)

        if not self._filter_text:
            return True

        if not nama:
            return True

        return self._filter_text in nama.lower()

    @Slot(str)  # pyright: ignore[reportAny]
    def filterPengajar(self, text: str) -> None:
        """Slot untuk mengatur filter teks pada proxy model."""
        self.setFilterFixedString(text)

    @Slot(int)  # pyright: ignore[reportAny]
    def removePengajarFromIndex(self, proxy_row: int) -> None:
        """Menghapus pengajar dengan aman menggunakan indeks dari proxy model."""
        if 0 <= proxy_row < self.rowCount():
            proxy_index = self.index(proxy_row, 0)
            source_index = self.mapToSource(proxy_index)
            self._pengajar_model.removePengajar(source_index.row())  # pyright: ignore[reportAny]

    # Gunakana QVariant agar QML bisa menerima dictionary
    @Slot(int, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def getPengajarFromProxyIndex(self, proxy_row: int):
        """Mengambil data pengajar dengan aman menggunakan indexks dari proxy model."""
        if 0 <= proxy_row < self.rowCount():
            proxy_index = self.index(proxy_row, 0)
            source_index = self.mapToSource(proxy_index)
            return self._pengajar_model.getPengajar(source_index.row())  # pyright: ignore[reportAny]

        return None

    @Slot(int, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def getPengajarFromSourceIndex(self, source_row: int):
        """Mengambil data pengajar dengan aman menggunakan indexks dari source model."""
        if 0 <= source_row < self._pengajar_model.rowCount():
            return self._pengajar_model.getPengajar(source_row)  # pyright: ignore[reportAny]

        return None
