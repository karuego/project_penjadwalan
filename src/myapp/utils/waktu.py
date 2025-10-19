from typing import override
from PySide6.QtCore import QObject, Property

NAMA_HARI: list[str] = [
    "_",
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat",
    "Sabtu",
    "Minggu",
]


class Hari:
    @staticmethod
    def getNama(id: int) -> str | None:
        if 0 < id < len(NAMA_HARI):
            return NAMA_HARI[id]
        return None

    @staticmethod
    def getId(nama: str) -> int:
        target: str = nama.lower()

        for i, s in enumerate(NAMA_HARI):
            if s.lower() == target:
                return i

        return -1

    @staticmethod
    def getAll() -> list[str]:
        return NAMA_HARI[1:]


class TimeSlot(QObject):
    def __init__(
        self,
        id: int = 0,
        hari: int = 0,
        mulai: str = "",
        selesai: str = "",
        createdAt: str = "",
        parent: QObject | None = None,
    ):
        super().__init__(parent)

        self._id: int = id
        self._hari: int = hari
        self._mulai: str = mulai
        self._selesai: str = selesai
        self._createdAt: str = createdAt

    def getId(self) -> int:
        return self._id

    def getHari(self) -> int:
        return self._hari

    def getMulai(self) -> str:
        return self._mulai

    def getSelesai(self) -> str:
        return self._selesai

    def getCreatedAt(self) -> str:
        return self._createdAt

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

    @Property(str)
    def createdAt(self) -> str:
        return self._createdAt

    def __iter__(self):
        return iter(
            {
                "id": self._id,
                "hari": self._hari,
                "mulai": self._mulai,
                "selesai": self._selesai,
                "createdAt": self._createdAt,
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
            case "createdAt":
                return self._createdAt
            case _:
                raise KeyError(f"Tidak ada atribut '{key}'")

    @override
    def __str__(self) -> str:
        return f"TimeSlot(id={self._id}, hari={self._hari}, mulai={self._mulai}, selesai={self._selesai}, createdAt={self._createdAt})"
