from myapp.utils.worker_scheduler import OptimizationWorker
import sqlite3
import typing
from result import Result, Ok, Err, is_ok, is_err

from PySide6.QtCore import (
    QAbstractTableModel,
    QByteArray,
    QModelIndex,
    QObject,
    QPersistentModelIndex,
    Qt,
    Slot,
    QThread,
    Signal,
)
from myapp import log
from myapp.utils import Database

from myapp.utils import sa as v6
from myapp.utils.struct_jadwal import Jadwal


class JadwalModel(QAbstractTableModel):
    # --- ROLE DEFINITIONS ---
    # Mendefinisikan cara QML mengakses data per kolom
    ID_ROLE: int = int(Qt.ItemDataRole.UserRole) + 1
    HARI_ROLE: int = int(Qt.ItemDataRole.UserRole) + 2
    JAM_ROLE: int = int(Qt.ItemDataRole.UserRole) + 3
    MATAKULIAH_ROLE: int = int(Qt.ItemDataRole.UserRole) + 4
    TIPE_ROLE: int = int(Qt.ItemDataRole.UserRole) + 5
    SKS_ROLE: int = int(Qt.ItemDataRole.UserRole) + 6
    SEMESTER_ROLE: int = int(Qt.ItemDataRole.UserRole) + 7
    KELAS_ROLE: int = int(Qt.ItemDataRole.UserRole) + 8
    RUANGAN_ROLE: int = int(Qt.ItemDataRole.UserRole) + 9
    DARING_ROLE: int = int(Qt.ItemDataRole.UserRole) + 10
    PENGAJAR_ROLE: int = int(Qt.ItemDataRole.UserRole) + 11

    # Signal untuk UI
    optimizationProgress: Signal = Signal(int, float, arguments=["iteration", "cost"])
    optimizationFinished: Signal = Signal(bool, str, arguments=["success", "message"])

    def __init__(self, db: Database, parent: QObject | None = None):
        super().__init__(parent)
        self.db: Database = db
        self._data: list[Jadwal] = []  # Data mentah
        self._filtered: list[Jadwal] = []  # Data yang ditampilkan (setelah filter)

        self._filter_query: str = ""
        self._filter_tipe: str = "semua"

        self.worker_thread = None
        self.worker = None

        self._headers: list[str] = [
            "ID",
            "Hari",
            "Jam",
            "Mata Kuliah",
            "Jenis",
            "SKS",
            "Semester",
            "Kelas",
            "Ruangan",
            "Daring",
            "Pengajar",
        ]

        # Load data awal
        self.loadDatabase()

    # ==========================================
    # BAGIAN WAJIB QABSTRACTTABLEMODEL (YANG HILANG)
    # ==========================================

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        # Mengembalikan jumlah baris berdasarkan data yang sudah difilter
        if parent.isValid():
            return 0
        return len(self._filtered)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._headers)

    def data(
        self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> typing.Any:
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if row < 0 or row >= len(self._filtered):
            return None

        item: Jadwal = self._filtered[row]

        # 1. HANDLE DISPLAY ROLE (Tampilan Teks Biasa di TableView)
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return str(item.getId())
            elif col == 1:
                return item.getHari()
            elif col == 2:
                return item.getJam()
            elif col == 3:
                return item.getMatakuliah()
            elif col == 4:
                return item.getJenis()
            elif col == 5:
                return str(item.getSks())
            elif col == 6:
                return str(item.getSemester())
            elif col == 7:
                return item.getKelas()
            elif col == 8:
                return item.getRuangan()
            elif col == 9:
                return "Online" if item.getDaring() else "Offline"
            elif col == 10:
                return item.getPengajar()

        # 2. HANDLE CUSTOM ROLES (Untuk akses via model.roleName di Delegate)
        elif role == self.ID_ROLE:
            return item.getId()
        elif role == self.HARI_ROLE:
            return item.getHari()
        elif role == self.JAM_ROLE:
            return item.getJam()
        elif role == self.MATAKULIAH_ROLE:
            return item.getMatakuliah()
        elif role == self.TIPE_ROLE:
            return item.getJenis()
        elif role == self.SKS_ROLE:
            return item.getSks()
        elif role == self.SEMESTER_ROLE:
            return item.getSemester()
        elif role == self.KELAS_ROLE:
            return item.getKelas()
        elif role == self.RUANGAN_ROLE:
            return item.getRuangan()
        elif role == self.DARING_ROLE:
            return item.getDaring()
        elif role == self.PENGAJAR_ROLE:
            return item.getPengajar()

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> typing.Any:
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            if 0 <= section < len(self._headers):
                return self._headers[section]
        return None

    def roleNames(self) -> dict[int, QByteArray]:
        # Mapping nama role di QML ke konstanta Role Python
        roles = super().roleNames()
        roles[self.ID_ROLE] = QByteArray(b"id_role")
        roles[self.HARI_ROLE] = QByteArray(b"hari")
        roles[self.JAM_ROLE] = QByteArray(b"jam")
        roles[self.MATAKULIAH_ROLE] = QByteArray(b"matakuliah")
        roles[self.TIPE_ROLE] = QByteArray(b"jenis")
        roles[self.SKS_ROLE] = QByteArray(b"sks")
        roles[self.SEMESTER_ROLE] = QByteArray(b"semester")
        roles[self.KELAS_ROLE] = QByteArray(b"kelas")
        roles[self.RUANGAN_ROLE] = QByteArray(b"ruangan")
        roles[self.DARING_ROLE] = QByteArray(b"daring")
        roles[self.PENGAJAR_ROLE] = QByteArray(b"pengajar")
        return roles

    # ==========================================
    # END BAGIAN WAJIB
    # ==========================================

    def setAllData(self, new_data: list[Jadwal]):
        """Memperbarui data dan mereset view."""
        self.beginResetModel()
        self._data = new_data
        self._filtered = new_data  # Default: tampilkan semua sebelum filter ulang
        self.endResetModel()

        # Terapkan ulang filter terakhir (misal: "teori")
        self.fnFilter(self._filter_query, self._filter_tipe)

    @Slot()
    def startOptimization(self):
        """Memulai proses generate jadwal di thread terpisah."""
        if self.worker_thread is not None and self.worker_thread.isRunning():
            log.warning("Optimasi sedang berjalan!")
            return

        v6.load_data()

        self.worker = OptimizationWorker(max_iter=5000)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.progress.connect(self._handle_progress)
        self.worker.finished.connect(self._handle_finished)
        self.worker.error.connect(self._handle_error)

        # Cleanup connections
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.finished.connect(self._cleanup_thread_references)

        self.worker_thread.start()

    def _handle_finished(self, raw_schedule: list, final_cost: float):
        log.info(f"Optimasi Selesai. Cost: {final_cost}")
        try:
            # 1. Simpan hasil mentah ke Database fisik (SQLite)
            # Fungsi ini ada di sa.py dan menerima list[ScheduleItem]
            log.info("Menyimpan jadwal ke database...")
            v6.save_schedule_to_db(raw_schedule)
            # ---------------------

            # 2. Konversi ke QObject (Jadwal) untuk ditampilkan di UI (Main Thread)
            jadwal_list = v6.convert_to_struct_objects(raw_schedule)
            self.setAllData(jadwal_list)  # Update UI

            msg = f"Jadwal berhasil dibuat dengan penalti: {final_cost:.2f}"
            self.optimizationFinished.emit(True, msg)
        except Exception as e:
            self._handle_error(f"Error converting result: {str(e)}")

    def _cleanup_thread_references(self):
        log.info("Membersihkan referensi thread.")
        self.worker_thread = None
        self.worker = None

    def _handle_error(self, error_msg: str):
        log.error(f"Optimasi Error: {error_msg}")
        self.optimizationFinished.emit(False, error_msg)
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.quit()

    def _handle_progress(self, iteration: int, cost: float):
        self.optimizationProgress.emit(iteration, cost)

    def fnFilter(self, query: str, tipe: str) -> None:
        """Filter data di memori."""
        q = query.strip().lower()
        t = tipe.strip().lower()

        self._filter_query = q
        self._filter_tipe = t

        self.beginResetModel()

        temp_filtered = []
        for item in self._data:
            # Logic Filter Tipe (Teori/Praktek/Semua)
            match_tipe = True
            if t != "semua" and t != "":
                # Pastikan getJenis() mengembalikan string yang sesuai ("teori"/"praktek")
                match_tipe = item.getJenis().lower() == t

            # Logic Filter Search Text
            match_nama = True
            if q:
                match_nama = (
                    q in item.getMatakuliah().lower() or q in item.getPengajar().lower()
                )

            if match_tipe and match_nama:
                temp_filtered.append(item)

        self._filtered = temp_filtered
        self.endResetModel()

    @Slot(str, str)
    def filter(self, query: str, tipe: str) -> None:
        self.fnFilter(query, tipe)

    def loadDatabase(self) -> None:
        semua_jadwal = self.db.get_all_jadwal()
        self.setAllData(semua_jadwal)
