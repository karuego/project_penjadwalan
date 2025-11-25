from result.result import Result
from result import Result, Ok, Err
import sqlite3
import typing
from typing import Literal
from PySide6.QtCore import (
    QAbstractListModel,
    QByteArray,
    QModelIndex,
    QObject,
    QPersistentModelIndex,
    Qt,
    Slot,
)
from utils.database import Database  # pyright: ignore[reportImplicitRelativeImport]
from utils.struct_ruangan import Ruangan  # pyright: ignore[reportImplicitRelativeImport]
import log # pyright: ignore[reportImplicitRelativeImport]


class RuanganModel(QAbstractListModel):
    ID_ROLE: int = int(Qt.ItemDataRole.UserRole) + 1
    NAMA_ROLE: int = int(Qt.ItemDataRole.UserRole) + 2
    TIPE_ROLE: int = int(Qt.ItemDataRole.UserRole) + 3

    def __init__(self, db: Database, parent: QObject | None = None):
        super().__init__(parent)
        self.db: Database = db
        self._data: list[Ruangan] = []

    @typing.override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> int | str | None:
        """
        Mengembalikan data untuk item dan role tertentu.
        """
        # beri tahu type checker bahwa kita perlakukan index sebagai QModelIndex
        idx: QModelIndex = typing.cast(QModelIndex, index)

        if not idx.isValid():
            return None

        item: Ruangan = self._data[idx.row()]
        # item: Ruangan = self._filtered[idx.row()]

        if role == self.ID_ROLE:
            return item.getId()
        if role == self.NAMA_ROLE:
            return item.getNama()
        if role == self.TIPE_ROLE:
            return item.getTipe()
        return None

    @typing.override
    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex | None = None,
    ) -> int:
        """
        Mengembalikan jumlah total item dalam model.
        """
        if parent is None:
            parent = QModelIndex()

        return len(self._data)
        # return len(self._filtered)

    @typing.override
    def roleNames(self) -> dict[int, QByteArray]:
        """
        Menghubungkan roles dengan nama yang akan digunakan di QML.
        """
        return {
            self.ID_ROLE: QByteArray(b"id_"),
            self.NAMA_ROLE: QByteArray(b"nama"),
            self.TIPE_ROLE: QByteArray(b"tipe"),
        }

    def addToList(self, ruang: Ruangan) -> None:
        """Method untuk menambahkan ruangan ke database."""
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(ruang)
        self.endInsertRows()

    def addToDatabase(self, ruang: Ruangan) -> Result[str, str]:
        """Method untuk menambahkan ruangan ke database."""
        try:
            # Validasi input
            if not all([ruang.getNama(), ruang.getTipe()]):
                return Err("Semua field harus diisi")

            # Insert ke database
            with self.db.get_connection() as conn:
                cursor: sqlite3.Cursor = conn.cursor()

                # Cek duplikasi nama ruangan
                query = "SELECT nama FROM ruangan WHERE nama LIKE ?"
                _ = cursor.execute(query, (ruang.getNama(),))
                data_lama: str | None = typing.cast(str|None, cursor.fetchone())

                if data_lama is not None:
                    return Err(f'Ruangan "{ruang.getNama()}" sudah ada.')

                _ = cursor.execute(
                    "INSERT INTO ruangan (nama, jenis) VALUES (?, ?)",
                    (ruang.getNama(), ruang.getTipe()),
                )

                id_ruang_baru: int | None = cursor.lastrowid
                if not id_ruang_baru:
                    log.info("Gagal menambahkan ruangan")
                    return Err("Gagal menambahkan ruangan")

                log.info(f"Ruangan '{ruang.getNama()}' dibuat dengan ID: {id_ruang_baru}")
                ruang.setId(id_ruang_baru)

                conn.commit()

            return Ok("Timeslot berhasil ditambahkan")

        except sqlite3.Error as e:
            return Err(f"Database error: {str(e)}")
        except Exception as e:
            return Err(f"Error: {str(e)}")

    def loadDatabase(self) -> None:
        ruangan: list[Ruangan] = self.db.get_all_ruangan()
        for ruang in ruangan:
            self.addToList(ruang)

    @Slot()  # pyright: ignore[reportAny]
    def reload(self) -> None:
        self.beginResetModel()
        self._data.clear()
        self.loadDatabase()
        self.endResetModel()

    def fnAdd(self, nama: str, is_lab: bool) -> Result[str, str]:
        """Method untuk menambahkan ruangan baru."""
        tipe: Literal['teori', 'praktek'] = "praktek" if is_lab else "teori"
        ruang: Ruangan = Ruangan(
            nama=nama,
            tipe=tipe
        )

        result: Result[str, str] = self.addToDatabase(ruang)
        if result.is_err():
            return result

        self.addToList(ruang)

        return Ok("Berhasil menambahkan ruangan baru.")

    @Slot(str, bool, result="QVariant")  # pyright: ignore[reportAny, reportArgumentType]
    def add(self, nama: str, is_lab: bool) -> dict[str, bool | str]:
        """Method QML untuk menambahkan ruangan baru."""
        result: Result[str, str] = self.fnAdd(nama, is_lab)

        success: bool = result.is_ok()
        message: str = result.unwrap() if success else result.unwrap_err()

        return {"success": success, "message": message}


    def fnGetIndex(self, index: int) -> Ruangan | None:
        if 0 <= index < len(self._data):
            return self._data[index]
        return None

    @Slot()  # pyright: ignore[reportAny]
    def getIndex(self, index: int) -> Ruangan | None:
        return self.fnGetIndex(index)

    def fnGetId(self, id: int) -> Ruangan | None:
        """
        Method untuk mengambil data pengajar berdasarkan id.
        """
        for item in self._data:
            if int(item.getId()) == int(id):
                print(item.id)
                return item

        return None

    @Slot(int, result=QObject)  # pyright: ignore[reportAny]
    def getId(self, id: int) -> Ruangan | None:
        return self.fnGetId(id)

    def getIndexById(self, id: int) -> int:
        for i, item in enumerate(self._data):
            if int(item.getId()) == int(id):
                return i

        return -1

    def fnRemoveIndex(self, index: int) -> None:
        """Method untuk menghapus pengajar berdasarkan index dari pada ListView QML."""
        if 0 <= index < self.rowCount():
            self.beginRemoveRows(QModelIndex(), index, index)
            del self._data[index]
            print(index)
            self.endRemoveRows()

    @Slot(int)  # pyright: ignore[reportAny]
    def removeIndex(self, index: int) -> None:
        self.fnRemoveIndex(index)

    def fnRemoveId(self, id: int) -> Result[str, str]:
        """Method untuk menghapus ruangan berdasarkan id."""
        index: int = self.getIndexById(id)

        self.beginRemoveRows(QModelIndex(), index, index)
        res: Result[str, str] = self.db.delete_ruangan(id)
        if res.is_err():
            return res

        del self._data[index]
        self.endRemoveRows()

    @Slot(int)  # pyright: ignore[reportAny]
    def removeId(self, id: int) -> dict[str, bool | str]:
        result: Result[str, str] = self.fnRemoveId(id)

        success: bool = result.is_ok()
        message: str = result.unwrap() if success else result.unwrap_err()

        return {"success": success, "message": message}
