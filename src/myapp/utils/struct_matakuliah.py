import re
from result import Result, Ok, Err, is_ok, is_err
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
        id: int,
        nama : str,
        tipe: str,
        semester: int,
        sks: int,
        kelas: int,
        sesi: int,
        pengampu: Pengajar,
        parent: QObject | None = None,
    ):
        super().__init__(parent)

        self._id: int = id
        self._nama: str = nama
        self._tipe: str = tipe
        self._semester: int = semester
        self._sks: int = sks
        self._jumlah_kelas: int = kelas
        self._jumlah_sesi_praktikum: int = sesi

        self._pengampu: Pengajar = pengampu

    def getId(self) -> int:
        return self._id

    def setId(self, id: int) -> None:
        self._id = id

    def getNama(self) -> str:
        return self._nama

    def setNama(self, nama: str) -> None:
        self._nama = nama.strip()

    def getTipe(self) -> str:
        return self._tipe

    def setTipe(self, tipe: str) -> bool:
        # TODO:
        t: str = tipe.strip().lower()
        if t not in TIPE_MATAKULIAH:
            return False
        self._tipe = t
        return True

    def getSemester(self) -> int:
        return self._semester

    def setSemester(self, n: int) -> None:
        self._semester = n

    def getSks(self) -> int:
        return self._semester

    def setSks(self, sks: int) -> None:
        self._semester = sks

    def getKelas(self) -> int:
        return self._jumlah_kelas

    def setKelas(self, n: int) -> None:
        self._jumlah_kelas = n

    def getSesi(self) -> int:
        return self._jumlah_sesi_praktikum

    def setSesi(self, n: int) -> None:
        self._jumlah_sesi_praktikum = n

    def getPengampu(self) -> Pengajar:
        return self._pengampu

    def setPengampu(self, pengajar: Pengajar) -> None:
        self._pengampu = pengajar

    def isValid(self) -> bool:
        if (
            self._id == 0
            or self._nama == ""
            or self._semester <= 0
            or self._sks <= 0
            or self._tipe == ""
            or self._jumlah_kelas <= 0
            or self._jumlah_sesi_praktikum <= 0
            or self._pengampu.isValid() is False
        ):
            return False
        return True

    def getAll(self) -> tuple[int, str, str, int, int, int, int, Pengajar]:
        return (
            self._id,
            self._nama,
            self._tipe,
            self._semester,
            self._sks,
            self._jumlah_kelas,
            self._jumlah_sesi_praktikum,
            self._pengampu,
        )

    @Property(int)
    def id(self) -> int:
        return self._id

    @Property(str)
    def nama(self) -> str:
        return self._nama

    @Property(str)
    def tipe(self) -> str:
        return self._tipe

    @Property(int)
    def semester(self) -> int:
        return self._semester

    @Property(int)
    def sks(self) -> int:
        return self._sks

    @Property(int)
    def kelas(self) -> int:
        return self._jumlah_kelas

    @Property(int)
    def sesi(self) -> int:
        return self._jumlah_sesi_praktikum

    @Property(dict)
    def pengampu(self) -> dict[str, str | int]:
        return {
            "id": self._pengampu.getId(),
            "nama": self._pengampu.getNama(),
            "tipe": self._pengampu.getTipe(),
            "waktu": self._pengampu.getWaktu()
        }

    def __iter__(self) -> Iterator[tuple[str, int | str | Pengajar]]:
        return iter(
            {
                "id": self._id,
                "nama": self._nama,
                "tipe": self._tipe,
                "semester": self._semester,
                "sks": self._sks,
                "kelas": self._jumlah_kelas,
                "sesi": self._jumlah_sesi_praktikum,
                "pengampu": self._pengampu
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
            case "semester":
                return self._semester
            case "sks":
                return self._sks
            case "kelas":
                return self._jumlah_kelas
            case "sesi":
                return self._jumlah_sesi_praktikum
            case "pengampu":
                return self._pengampu
            case _:
                raise KeyError(f"Tidak ada atribut '{key}'")

    @override
    def __str__(self) -> str:
        return f'MataKuliah(id="{self._id}", nama="{self._nama}", tipe="{self._tipe}", semester="{self._semester}, sks="{self._sks}", kelas="{self._jumlah_kelas}", sesi="{self._jumlah_sesi_praktikum}", pengampu="{self._pengampu}")'
