import typing
from PySide6.QtCore import (
    QObject,
    QModelIndex,
    QPersistentModelIndex,
    QSortFilterProxyModel,
)
from . import PengajarModel


class FilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._filter_text: str = ""

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

        if nama is None:
            return False

        return self._filter_text in nama.lower()
