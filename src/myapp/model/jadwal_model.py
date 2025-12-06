from myapp.utils.struct_jadwal import Jadwal
from myapp.utils.worker_scheduler import OptimizationWorker
from typing import override
from result import Result, Ok, Err, is_ok, is_err

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Flowable,
)
from reportlab.lib.styles import getSampleStyleSheet

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
    QUrl,
)
from myapp import log
from myapp.utils import Database
from myapp.utils import sa as v6
from myapp.utils.hari import Hari
from myapp.utils.struct_jadwal import Jadwal
from myapp.utils.schedule_item import ScheduleItem


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

        self.worker_thread: QThread | None = None
        self.worker: OptimizationWorker | None = None

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
            "Metode",
            "Pengajar",
        ]

        # Load data awal
        self.loadDatabase()

    # ==========================================
    # BAGIAN WAJIB QABSTRACTTABLEMODEL (YANG HILANG)
    # ==========================================

    @override
    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = QModelIndex(),  # pyright: ignore[reportCallInDefaultInitializer]
    ) -> int:
        # Mengembalikan jumlah baris berdasarkan data yang sudah difilter
        if parent.isValid():
            return 0

        return len(self._filtered)

    @override
    def columnCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = QModelIndex(),  # pyright: ignore[reportCallInDefaultInitializer]
    ) -> int:
        if parent.isValid():
            return 0

        return len(self._headers)

    @override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> int | str | None:
        if not index.isValid():
            return None

        row: int = index.row()
        col: int = index.column()

        if row < 0 or row >= len(self._filtered):
            return None

        item: Jadwal = self._filtered[row]

        return {
            # HANDLE DISPLAY ROLE
            #    (Tampilan Teks Biasa di TableView)
            Qt.ItemDataRole.DisplayRole: self._handle_display_role(item, col),
            # HANDLE CUSTOM ROLES
            #    (Untuk akses via model.roleName di Delegate)
            self.ID_ROLE: item.getId(),
            self.HARI_ROLE: item.getHari(),
            self.JAM_ROLE: item.getJam(),
            self.MATAKULIAH_ROLE: item.getMatakuliah(),
            self.TIPE_ROLE: item.getJenis(),
            self.SKS_ROLE: item.getSks(),
            self.SEMESTER_ROLE: item.getSemester(),
            self.KELAS_ROLE: item.getKelas(),
            self.RUANGAN_ROLE: item.getRuangan(),
            self.DARING_ROLE: item.getDaring(),
            self.PENGAJAR_ROLE: item.getPengajar(),
        }.get(role, None)

    def _handle_display_role(self, item: Jadwal, col: int) -> str | None:
        return {
            0: str(item.getId()),
            1: item.getHari(),
            2: item.getJam(),
            3: item.getMatakuliah(),
            4: item.getJenis(),
            5: str(item.getSks()),
            6: str(item.getSemester()),
            7: item.getKelas(),
            8: item.getRuangan(),
            9: "Online" if item.getDaring() else "Offline",
            10: item.getPengajar(),
        }.get(col, None)

    @override
    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            if 0 <= section < len(self._headers):
                return self._headers[section]
        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        # Mapping nama role di QML ke konstanta Role Python
        roles: dict[int, QByteArray] = super().roleNames()
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
        """Memperbarui data, mengurutkannya, dan mereset view."""

        # LOGIKA SORTING:
        # Key 1: Hari.getId(x.getHari()) -> Mengubah "Senin" jadi 1, "Selasa" jadi 2, dst.
        # Key 2: x.getJam() -> Mengurutkan string jam ("07:00" < "09:00")
        new_data.sort(key=lambda x: (Hari.getId(x.getHari()), x.getJam()))

        self.beginResetModel()
        self._data = new_data
        self._filtered = new_data  # Default: tampilkan semua sebelum filter ulang
        self.endResetModel()

        # Terapkan ulang filter terakhir (misal: "teori")
        self.fnFilter(self._filter_query, self._filter_tipe)

    @Slot()  # pyright: ignore[reportAny]
    def startOptimization(self):
        """Memulai proses generate jadwal di thread terpisah."""
        if self.worker_thread is not None and self.worker_thread.isRunning():
            log.warning("Optimasi sedang berjalan!")
            return

        v6.load_data()

        self.worker = OptimizationWorker(max_iter=10000)
        self.worker_thread = QThread()
        _ = self.worker.moveToThread(self.worker_thread)

        _ = self.worker_thread.started.connect(self.worker.run)
        _ = self.worker.progress.connect(self._handle_progress)
        _ = self.worker.finished.connect(self._handle_finished)
        _ = self.worker.error.connect(self._handle_error)

        # Cleanup connections
        _ = self.worker.finished.connect(self.worker_thread.quit)
        _ = self.worker.finished.connect(self.worker.deleteLater)
        _ = self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        _ = self.worker_thread.finished.connect(self._cleanup_thread_references)

        self.worker_thread.start()

    def _handle_finished(self, raw_schedule: list[ScheduleItem], final_cost: float):
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

        temp_filtered: list[Jadwal] = []
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

    @Slot(str, str)  # pyright: ignore[reportAny]
    def filter(self, query: str, tipe: str) -> None:
        self.fnFilter(query, tipe)

    @Slot(str, str)  # pyright: ignore[reportAny]
    def exportToPdf(self, file_url: str, tipe: str):
        """
        Mengekspor jadwal ke PDF.
        file_url: Path file dari FileDialog QML (format file:///...)
        tipe: 'teori' atau 'praktek'
        """
        try:
            # 1. Konversi URL QML ke Path Lokal OS
            file_path: str = QUrl(file_url).toLocalFile()
            if not file_path:
                # Fallback jika QUrl gagal (misal di OS tertentu stringnya raw)
                file_path = file_url.replace("file://", "")

            # Tambahkan ekstensi .pdf jika belum ada
            if not file_path.lower().endswith(".pdf"):
                file_path += ".pdf"

            log.info(f"Mengekspor PDF ke: {file_path}")

            # 2. Siapkan Data (Filter & Sort)
            # Kita gunakan logika filter manual agar tidak mengganggu tampilan tabel utama
            target_tipe: str = tipe.lower().strip()
            data_export: list[Jadwal] = []

            # Ambil data dari source utama (self._data)
            for item in self._data:
                # Filter Tipe
                if target_tipe == "teori" and item.getJenis().lower() != "teori":
                    continue
                if target_tipe == "praktek" and item.getJenis().lower() != "praktek":
                    continue
                data_export.append(item)

            # Sort: Hari -> Jam
            data_export.sort(key=lambda x: (Hari.getId(x.getHari()), x.getJam()))

            # 3. Buat Dokumen PDF (Landscape agar muat banyak kolom)
            doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
            elements: list[Flowable] = []
            styles = getSampleStyleSheet()

            # Judul
            judul_text: str = f"Jadwal Kuliah - {tipe.capitalize()}"
            elements.append(Paragraph(judul_text, styles["Title"]))
            elements.append(Spacer(1, 20))

            # Header Tabel
            table_data: list[list[str]] = [
                [
                    "Hari",
                    "Jam",
                    "Mata Kuliah",
                    # "SKS",
                    "Kls",
                    "Ruangan",
                    "Pengajar",
                    # "Ket",
                ]
            ]

            # Isi Tabel
            for item in data_export:
                lokasi: str = "Online" if item.getDaring() else item.getRuangan()
                row: list[str] = [
                    item.getHari(),
                    item.getJam(),
                    item.getMatakuliah(),
                    # str(item.getSks()),
                    item.getKelas(),
                    lokasi,
                    item.getPengajar(),
                    # item.getJenis().capitalize(),
                ]
                table_data.append(row)

            # 4. Styling Tabel ReportLab
            # (Lebar kolom disesuaikan secara proporsional)
            # col_widths: list[int] = [50, 80, 200, 30, 30, 80, 150, 50]
            col_widths: list[int] = [50, 80, 200, 30, 80, 300]

            t = Table(table_data, colWidths=col_widths)
            t.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.grey,
                        ),  # Header warna abu
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, 0),
                            colors.whitesmoke,
                        ),  # Text Header putih
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        (
                            "BACKGROUND",
                            (0, 1),
                            (-1, -1),
                            colors.beige,
                        ),  # Baris data warna beige
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Garis tabel
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("FONTSIZE", (0, 1), (-1, -1), 8),  # Font isi lebih kecil
                    ]
                )
            )

            elements.append(t)

            # 5. Build
            doc.build(elements)

            self.optimizationFinished.emit(
                True, f"PDF berhasil disimpan di:\n{file_path}"
            )

        except Exception as e:
            log.error(f"Gagal ekspor PDF: {str(e)}")
            self.optimizationFinished.emit(False, f"Gagal ekspor PDF: {str(e)}")

    def loadDatabase(self) -> None:
        semua_jadwal: list[Jadwal] = self.db.get_all_jadwal()
        self.setAllData(semua_jadwal)
