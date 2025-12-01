from typing import override
from collections.abc import Iterator
from PySide6.QtCore import QObject, Property


class Jadwal(QObject):
    def __init__(
        self,
        id: int,
        hari: str,
        jam: str,
        matakuliah: str,
        jenis: str,
        sks: int,
        semester: int,
        kelas: str,
        ruangan: str,
        daring: bool,
        pengajar: str,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        self._id: int = id
        self._hari: str = hari
        self._jam: str = jam
        self._matakuliah: str = matakuliah
        self._jenis: str = jenis
        self._sks: int = sks
        self._semester: int = semester
        self._kelas: str = kelas
        self._ruangan: str = ruangan
        self._daring: bool = daring
        self._pengajar: str = pengajar

    def getId(self) -> int:
        return self._id

    def setId(self, id: int) -> None:
        self._id = id

    def getHari(self) -> str:
        return self._hari

    def setHari(self, hari: str) -> None:
        self._hari = hari

    def getJam(self) -> str:
        return self._jam

    def setJam(self, jam: str) -> None:
        self._jam = jam

    def getMatakuliah(self) -> str:
        return self._matakuliah

    def setMatakuliah(self, matkul: str) -> None:
        self._matakuliah = matkul

    def getJenis(self) -> str:
        return self._jenis

    def setJenis(self, jenis: str) -> None:
        self._matakuliah = jenis

    def getSks(self) -> int:
        return self._sks

    def setSks(self, sks: int) -> None:
        self._sks = sks

    def getSemester(self) -> int:
        return self._semester

    def setSemester(self, smt: int) -> None:
        self._semester = smt

    def getKelas(self) -> str:
        return self._kelas

    def setKelas(self, kelas: str) -> None:
        self._kelas = kelas

    def getRuangan(self) -> str:
        return self._ruangan

    def setRuangan(self, ruang: str) -> None:
        self._ruangan = ruang

    def getDaring(self) -> int:
        return self._daring

    def setDaring(self, daring: bool) -> None:
        self._daring = daring

    def getPengajar(self) -> str:
        return self._pengajar

    def setPengajar(self, nama: str) -> None:
        self._pengajar = nama

    def get(self, key: str, default: int | str) -> int | str:
        try:
            return self[key]  # Memanggil __getitem__
        except KeyError:
            return default

    def getAll(self) -> tuple[int, str, str, str, str, int, int, str, str, bool, str]:
        return (
            self._id,
            self._hari,
            self._jam,
            self._matakuliah,
            self._jenis,
            self._sks,
            self._semester,
            self._kelas,
            self._ruangan,
            self._daring,
            self._pengajar,
        )

    id: Property = Property(int, getId, None, None, "")
    hari: Property = Property(str, getHari, None, None, "")
    jam: Property = Property(str, getJam, None, None, "")
    matakuliah: Property = Property(str, getMatakuliah, None, None, "")
    jenis: Property = Property(str, getJenis, None, None, "")
    sks: Property = Property(int, getSks, None, None, "")
    semester: Property = Property(int, getSemester, None, None, "")
    kelas: Property = Property(str, getKelas, None, None, "")
    ruangan: Property = Property(str, getRuangan, None, None, "")
    daring: Property = Property(int, getDaring, None, None, "")
    pengajar: Property = Property(str, getPengajar, None, None, "")

    _keys: list[str] = [
        "id",
        "hari",
        "jam",
        "matakuliah",
        "jenis",
        "sks",
        "semester",
        "kelas",
        "ruangan",
        "daring",
        "pengajar",
    ]

    def __iter__(self) -> Iterator[tuple[str, int | str]]:
        for key in self._keys:
            # yield akan "menyerahkan" data satu per satu saat diminta
            # Tidak ada dictionary yang dibuat di sini. Hemat memori.
            val = getattr(self, f"_{key}")  # pyright: ignore[reportAny]
            yield (key, val)

    def __getitem__(self, key: str) -> int | str:
        try:
            # Mengambil atribut self._key secara dinamis
            return getattr(self, f"_{key}")  # pyright: ignore[reportAny]
        except AttributeError:
            # Ubah error 'Attribute not found' menjadi 'Key not found' agar konsisten
            raise KeyError(f"Tidak ada atribut '{key}'")

    @override
    def __str__(self) -> str:
        parts: list[str] = []
        for key in self._keys:
            val: int | str = getattr(self, f"_{key}")  # pyright: ignore[reportAny]
            # !r akan otomatis menambahkan kutip jika val adalah string (repr)
            parts.append(f"{key}={val!r}")

        return f"Jadwal({', '.join(parts)})"
