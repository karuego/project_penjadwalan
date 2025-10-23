from typing import cast, override
from PySide6.QtCore import (
    Slot,
    Qt,
    QObject,
    QModelIndex,
    QPersistentModelIndex,
    QSortFilterProxyModel,
)

from .waktu_model import WaktuModel


class WaktuProxyModel(QSortFilterProxyModel):
    def __init__(self, model: WaktuModel, parent: QObject | None = None):
        super().__init__(parent)
        self._model: WaktuModel = model

        # TODO: tambahkan filter untuk waktu mulai
        self.setSourceModel(self._model)
        self.setFilterRole(WaktuModel.HARI_ROLE)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownMemberType]

    @override
    def lessThan(
        self,
        left: QModelIndex | QPersistentModelIndex,
        right: QModelIndex | QPersistentModelIndex,
    ) -> bool:
        model: WaktuModel = cast(WaktuModel, self.sourceModel())
        hari_left: int = cast(int, model.data(left, WaktuModel.HARI_ROLE))
        hari_right: int = cast(int, model.data(right, WaktuModel.HARI_ROLE))

        if hari_left == hari_right:
            mulai_left: str = cast(str, model.data(left, WaktuModel.MULAI_ROLE))
            mulai_right: str = cast(str, model.data(right, WaktuModel.MULAI_ROLE))
            return mulai_left < mulai_right

        return hari_left < hari_right

    @Slot(int)  # pyright: ignore[reportAny]
    def removeFromIndex(self, proxy_row: int) -> None:
        """Menghapus pengajar dengan aman menggunakan indeks dari proxy model."""
        if 0 <= proxy_row < self.rowCount():
            proxy_index: QModelIndex = self.index(proxy_row, 0)
            source_index: QModelIndex = self.mapToSource(proxy_index)
            self._model.fnRemoveIndex(source_index.row())

    # Gunakana QVariant agar QML bisa menerima dictionary
    @Slot(int, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def getByProxyIndex(self, proxy_row: int):
        """Mengambil data pengajar dengan aman menggunakan indexks dari proxy model."""
        if 0 <= proxy_row < self.rowCount():
            proxy_index: QModelIndex = self.index(proxy_row, 0)
            source_index: QModelIndex = self.mapToSource(proxy_index)
            return self._model.fnGetIndex(source_index.row())

        return None

    @Slot(int, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def getSourceIndex(self, source_row: int):
        """Mengambil data pengajar dengan aman menggunakan indeks dari source model."""
        if 0 <= source_row < self._model.rowCount():
            return self._model.fnGetIndex(source_row)

        return None
