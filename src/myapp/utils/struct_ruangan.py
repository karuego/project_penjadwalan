from typing import override
from PySide6.QtCore import QObject, Property


class Ruangan(QObject):
    def __init__(
        self,
        id: str = "",
        nama: str = "",
        tipe: str = "",
        parent: QObject | None = None,
    ):
        super().__init__(parent)

        self._id: str = id
        self._nama: str = nama
        self._tipe: str = tipe

    def getId(self) -> str:
        return self._id

    def setId(self, id: str) -> None:
        self._id = id

    def getNama(self) -> str:
        return self._nama

    def setNama(self, nama: str) -> None:
        self._nama = nama

    def getTipe(self) -> str:
        return self._tipe

    def setTipe(self, tipe: str) -> None:
        self._tipe = tipe

    def isValid(self) -> bool:
        if str(self._id) == "" or str(self._nama) == "" or str(self._tipe) == "":
            return False
        return True

    @Property(str)
    def id(self) -> str:
        return self._id

    @Property(int)
    def nama(self) -> str:
        return self._nama

    @Property(str)
    def tipe(self) -> str:
        return self._tipe

    def __iter__(self):
        return iter(
            {
                "id": self._id,
                "nama": self._nama,
                "tipe": self._tipe,
            }.items()
        )

    def __getitem__(self, key: str) -> int | str | None:
        match key:
            case "id":
                return self._id
            case "nama":
                return self._nama
            case "tipe":
                return self._tipe
            case _:
                raise KeyError(f"Tidak ada atribut '{key}'")

    @override
    def __str__(self) -> str:
        return f"TimeSlot(id={self._id}, nama={self._nama}, tipe={self._tipe})"
