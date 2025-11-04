import re
from enum import Enum
from typing import override
from PySide6.QtCore import QObject, Property


# TODO: ganti jadi list[dict[str, str]]
# [{ 'text': 'Dosen', 'value': 'dosen' }, { 'text': 'Asisten Dosen', 'value': 'asdos' }]
TIPE_PENGAJAR: list[str] = ["dosen", "asdos"]


class TipePengajar(Enum):
    DOSEN = "dosen"
    ASDOS = "asdos"


class Pengajar(QObject):
    def __init__(
        self,
        id: str = "",
        nama: str = "",
        tipe: str = "",
        waktu: str = "",
        parent: QObject | None = None,
    ):
        super().__init__(parent)

        self._id: str = id.strip()
        self._nama: str = nama.strip()
        self._tipe: str = tipe.strip().lower()
        self._waktu: str = re.sub(r"\s+", "", waktu.strip())

    def getId(self) -> str:
        return self._id

    def setId(self, id: str) -> None:
        self._id = id.strip()

    def getNama(self) -> str:
        return self._nama

    def setNama(self, nama: str) -> None:
        self._nama = nama.strip()

    def getTipe(self) -> str:
        return self._tipe

    def setTipe(self, tipe: str) -> bool:
        # TODO:
        t: str = tipe.strip().lower()
        if t not in TIPE_PENGAJAR:
            return False
        self._tipe = t
        return True

    def getWaktu(self) -> str:
        return self._waktu

    def setWaktu(self, waktu: str) -> None:
        self._waktu = re.sub(r"\s+", "", waktu.strip())

    def isValid(self) -> bool:
        if (
            str(self._id) == ""
            or str(self._nama) == ""
            or str(self._tipe) == ""
            or str(self._waktu) == ""
        ):
            return False
        return True

    @Property(str)
    def id(self) -> str:
        return self._id

    @Property(str)
    def nama(self) -> str:
        return self._nama

    @Property(str)
    def tipe(self) -> str:
        return self._tipe

    @Property(str)
    def waktu(self) -> str:
        return re.sub(r"\s+", "", self._waktu.strip())

    def __iter__(self):
        return iter(
            {
                "id": self._id,
                "nama": self._nama,
                "tipe": self._tipe,
                "waktu": self._waktu,
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
            case "waktu":
                return self._waktu
            case _:
                raise KeyError(f"Tidak ada atribut '{key}'")

    @override
    def __str__(self) -> str:
        return f'Pengajar(id="{self._id}", nama="{self._nama}", tipe="{self._tipe}", waktu="{self._waktu}")'
