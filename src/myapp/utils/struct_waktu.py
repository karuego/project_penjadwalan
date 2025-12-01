from typing import override
from PySide6.QtCore import QObject, Property

from .hari import Hari


class TimeSlot(QObject):
    def __init__(
        self,
        id: int = -1,
        hari: int = 0,
        mulai: str = "",
        selesai: str = "",
        parent: QObject | None = None,
    ):
        super().__init__(parent)

        self._id: int = id
        self._hari: int = hari
        self._mulai: str = mulai
        self._selesai: str = selesai

    def getId(self) -> int:
        return self._id

    def setId(self, id: int) -> None:
        self._id = id

    def getHari(self) -> int:
        """Mengembalikan id hari"""
        return self._hari

    def getHariName(self) -> str | None:
        """Mengembalikan nama hari"""
        return Hari.getNama(self._id)

    def setHari(self, hari: int) -> bool:
        if not Hari.getNama(hari):
            return False
        self._hari = hari
        return True

    def setHariName(self, hari: str) -> bool:
        hari_id: int = Hari.getId(hari)
        if hari_id == -1:
            return False
        self._hari = hari_id
        return True

    def getMulai(self) -> str:
        return self._mulai

    def setMulai(self, mulai: str) -> None:
        self._mulai = mulai

    def getSelesai(self) -> str:
        return self._selesai

    def setSelesai(self, selesai: str) -> None:
        self._selesai = selesai

    def isEmpty(self) -> bool:
        if self._id <= 0:
            return True
        if not Hari.getNama(self._hari):
            return True
        if self._mulai != "" or self._selesai != "":
            return True
        return False

    @Property(int)
    def id(self) -> int:
        return self._id

    @Property(int)
    def hari(self) -> int:
        return self._hari

    @Property(str)
    def mulai(self) -> str:
        return self._mulai

    @Property(str)
    def selesai(self) -> str:
        return self._selesai

    def __iter__(self):
        return iter(
            {
                "id": self._id,
                "hari": self._hari,
                "mulai": self._mulai,
                "selesai": self._selesai,
            }.items()
        )

    def __getitem__(self, key: str) -> int | str | None:
        match key:
            case "id":
                return self._id
            case "hari":
                return self._hari
            case "mulai":
                return self._mulai
            case "selesai":
                return self._selesai
            case _:
                raise KeyError(f"Tidak ada atribut '{key}'")

    @override
    def __str__(self) -> str:
        return f"TimeSlot(id={self._id}, hari={self._hari}, mulai={self._mulai}, selesai={self._selesai})"
