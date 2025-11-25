from enum import Enum
from typing import override
from collections.abc import Iterator
from PySide6.QtCore import QObject, Property
from .struct_pengajar import Pengajar

TIPE_MATAKULIAH: list[str] = ["teori", "praktek"]

class TipeMataKuliah(Enum):
    TEORI = "teori"
    PRAKTEK = "praktek"

class MataKuliah(QObject):
    def __init__(
        self,
        id: int | None = None,
        nama : str | None = None,
        tipe: str | None = None,
        sks: int | None = None,
        semester: int | None = None,
        kelas: int|None = None,
        pengampu: Pengajar | None = None,
        parent: QObject | None = None,
    ):
        super().__init__(parent)

        self._id: int | None = id
        self._nama: str | None = nama
        self._tipe: str | None = tipe
        self._sks: int | None = sks
        self._semester: int | None = semester
        self._jumlah_kelas: int | None = kelas

        self._pengampu: Pengajar | None = pengampu

    def getId(self) -> int | None:
        return self._id

    def setId(self, id: int | None) -> None:
        self._id = id

    def getNama(self) -> str | None:
        return self._nama

    def setNama(self, nama: str | None) -> None:
        self._nama = None if nama is None else nama.strip()

    def getTipe(self) -> str | None:
        return self._tipe

    def setTipe(self, tipe: str | None) -> bool:
        # TODO:
        t: str = "unknown" if tipe is None else tipe.strip().lower()
        if t not in TIPE_MATAKULIAH:
            return False
        self._tipe = t
        return True

    def getSks(self) -> int | None:
        return self._sks

    def setSks(self, sks: int | None) -> None:
        self._sks = sks

    def getSemester(self) -> int | None:
        return self._semester

    def setSemester(self, smt: int | None) -> None:
        self._semester = smt

    def getKelas(self) -> int | None:
        return self._jumlah_kelas

    def setKelas(self, n: int | None) -> None:
        self._jumlah_kelas = n

    def getPengampu(self) -> Pengajar | None:
        return self._pengampu

    def setPengampu(self, pengajar: Pengajar | None) -> None:
        self._pengampu = pengajar

    def isValid(self) -> bool:
        if (
            self._id is None
            or self._nama is None
            or self._tipe is None
            or self._sks is None
            or self._semester is None
            or self._jumlah_kelas is None
            or self._pengampu is None
            or not self._pengampu.isValid()
        ):
            return False
        return True

    def getAll(self) -> tuple[int|None, str|None, str|None, int|None, int|None, int|None, Pengajar|None]:
        return (
            self._id,
            self._nama,
            self._tipe,
            self._sks,
            self._semester,
            self._jumlah_kelas,
            self._pengampu,
        )

    @Property(int)
    def id(self) -> int|None:
        return self._id

    @Property(str)
    def nama(self) -> str|None:
        return self._nama

    @Property(str)
    def tipe(self) -> str|None:
        return self._tipe

    @Property(int)
    def sks(self) -> int|None:
        return self._sks

    @Property(int)
    def semester(self) -> int|None:
        return self._semester

    @Property(int)
    def kelas(self) -> int|None:
        return self._jumlah_kelas

    @Property(dict)
    def pengampu(self) -> dict[str, str | int] |None:
        if self._pengampu is None:
            return None

        return {
            "id": self._pengampu.getId(),
            "nama": self._pengampu.getNama(),
            "tipe": self._pengampu.getTipe(),
            "waktu": self._pengampu.getWaktu()
        }

    def __iter__(self) -> Iterator[tuple[str, int | str | Pengajar | None]]:
        return iter(
            {
                "id": self._id,
                "nama": self._nama,
                "tipe": self._tipe,
                "sks": self._sks,
                "semester": self._semester,
                "kelas": self._jumlah_kelas,
                "pengampu": self._pengampu,
            }.items()
        )

    def __getitem__(self, key: str) -> int | str | Pengajar | None:
        match key:
            case "id":
                return self._id
            case "nama":
                return self._nama
            case "tipe":
                return self._tipe
            case "sks":
                return self._sks
            case "semester":
                return self._semester
            case "kelas":
                return self._jumlah_kelas
            case "pengampu":
                return self._pengampu
            case _:
                raise KeyError(f"Tidak ada atribut '{key}'")

    @override
    def __str__(self) -> str:
        return f'MataKuliah(id={self._id}, nama="{self._nama}", tipe="{self._tipe}", sks={self._sks}, semester={self._semester}, kelas={self._jumlah_kelas}, pengampu="{str(self._pengampu)}")'
