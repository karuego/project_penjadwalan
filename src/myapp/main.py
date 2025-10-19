# This Python file uses the following encoding: utf-8
import sys
import signal
import logging
from pathlib import Path

from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine, QQmlError, qmlRegisterType

# import resources_rc

from model import MataKuliahModel, PengajarModel, WaktuModel  # pyright: ignore[reportImplicitRelativeImport]
from bridge import ContextBridge  # pyright: ignore[reportImplicitRelativeImport]
from utils import (  # pyright: ignore[reportImplicitRelativeImport]
    Database,
    TimeSlot,
)

# Konfigurasi logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger: logging.Logger = logging.getLogger(__name__)


def handle_qml_error(err: QQmlError) -> None:
    logger.error(
        f"QML Error at {err.url().toString()}:{err.line()} — {err.description()}"
    )


def on_qml_warning(errors: list[QQmlError]) -> None:
    for e in errors:
        handle_qml_error(e)


def run() -> None:
    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon("src/myapp/assets/icon.png"))
    engine = QQmlApplicationEngine()

    # Kembalikan perilaku SIGINT default agar Ctrl+C mematikan proses
    _ = signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Log QML error
    # _ = engine.warnings.connect(on_qml_warning)

    # log_bridge: LogBridge = LogBridge(logger)
    # logger.addHandler(logging.StreamHandler(log_bridge))
    # _ = log_bridge.logMessage.connect(lambda m: print(f"From QML: {m}"))
    # engine.rootContext().setContextProperty("LogBridge", log_bridge)

    # Tentukan path ke direktori yang berisi modul QML Anda
    qml_dir: Path = Path(__file__).resolve().parent / "qml"

    # Beritahu engine untuk mencari modul di dalam direktori 'qml/'
    engine.addImportPath(str(qml_dir))

    db: Database = Database()

    data_pengajar: list[dict[str, str]] = [
        {
            "id_": "123000001",
            "nama": "Dr. Budi Santoso",
            "tipe": "dosen",
            "waktu": "1,2",
        },
        {
            "id_": "123000002",
            "nama": "Prof. Ika Wijayanti",
            "tipe": "dosen",
            "waktu": "2,3",
        },
        {
            "id_": "123000003",
            "nama": "Ahmad Abdullah, M.Kom",
            "tipe": "dosen",
            "waktu": "",
        },
        {"id_": "000000001", "nama": "Asisten 1", "tipe": "asdos", "waktu": "3,4"},
        {"id_": "000000002", "nama": "Asisten 2", "tipe": "asdos", "waktu": "3,5"},
        {"id_": "000000003", "nama": "Asisten 3", "tipe": "asdos", "waktu": "1,5"},
        {"id_": "000000004", "nama": "Asisten 4", "tipe": "asdos", "waktu": "1,2"},
        {"id_": "000000005", "nama": "Asisten 5", "tipe": "asdos", "waktu": "4,6"},
        {"id_": "000000006", "nama": "Asisten 6", "tipe": "asdos", "waktu": ""},
    ]

    # Inisialisasi model pengajar
    pengajar_model: PengajarModel = PengajarModel(data_pengajar)

    # Inisialisasi proxy model
    pengajar_proxy_model = QSortFilterProxyModel()
    pengajar_proxy_model.setSourceModel(pengajar_model)
    pengajar_proxy_model.setFilterRole(PengajarModel.TIPE_ROLE)
    pengajar_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownMemberType]

    # Menambahkan beberapa data pengajar
    # pengajar_model.addPengajar("Dr. Budi Santoso", "Dosen", "1,2")
    # pengajar_model.addPengajar("Prof. Ika Wijayanti", "Dosen", "2,3")
    # pengajar_model.addPengajar("Ahmad Abdullah, M.Kom", "Dosen", "")
    # pengajar_model.addPengajar("Asisten 1", "Asdos", "3,4")
    # pengajar_model.addPengajar("Asisten 2", "Asdos", "3,5")

    matakuliah_model = MataKuliahModel()

    # Buat instance dari WaktuModel
    waktu_model: WaktuModel = WaktuModel(db)

    # Tambahkan beberapa data awal untuk contoh
    # waktu_model.addWaktu("Selasa", "10:00", "11:40")
    # waktu_model.addWaktu("Rabu", "13:00", "14:40")

    all_timeslots: list[TimeSlot] = db.timeslot_manager.get_all_timeslots()
    # print(all_timeslots)
    # exit()

    for timeslot in all_timeslots:
        # waktu_model.addWaktu(timeslot.hari, timeslot.mulai, timeslot.selesai)
        waktu_model.addTimeSlot(timeslot)  # pyright: ignore[reportAny]

    qmlRegisterType(TimeSlot, "MyModule", 1, 0, "TimeSlot")  # pyright: ignore[reportCallIssue, reportArgumentType]

    # Buat instance dari bridge dan ekspos ke QML
    context_bridge = ContextBridge(
        waktu_model, pengajar_model, pengajar_proxy_model, matakuliah_model
    )

    # engine.rootContext().setContextProperty("waktuModel", waktu_model)
    engine.rootContext().setContextProperty("contextBridge", context_bridge)

    qml_file: Path = qml_dir / "Main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    logger.info("Aplikasi dimulai.")
    _ = app.exec()


if __name__ == "__main__":
    run()
