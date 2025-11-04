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

        for i, s in enumerate(NAMA_HARI, start=1):
            if s.lower() == target:
                return i

        return -1

    @staticmethod
    def getAll() -> list[str]:
        return NAMA_HARI[1:]

    @staticmethod
    def getAllId() -> list[int]:
        return list(range(1, len(NAMA_HARI)))
