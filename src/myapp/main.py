# This Python file uses the following encoding: utf-8
import os
import logging
import signal
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine, QQmlError, qmlRegisterType

from myapp.context import ContextBridge
from myapp.utils import (
    TimeSlot,
    Database,
    TimeSlotManager,
    ScheduleGenerator,
)

# import resources_rc

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
    db = Database()
    # timeslot_manager: TimeSlotManager = TimeSlotManager(db)
    # schedule_generator: ScheduleGenerator = ScheduleGenerator(
    #     timeslot_manager
    # )
    if not db.is_exist():
        db.init_database()
        # # total_generated, results = schedule_generator.generate_schedule()
        # _ = schedule_generator.generate_schedule()

    app = QGuiApplication(sys.argv)
    # app.setWindowIcon(
    #     QIcon(
    #         "/home/kae/Studio/Git/karuego/project_penjadwalan/src/myapp/assets/icon2.png"
    #     )
    # )
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

    qmlRegisterType(TimeSlot, "MyModule", 1, 0, "TimeSlot")  # pyright: ignore[reportCallIssue, reportArgumentType]

    # Buat instance dari bridge dan ekspos ke QML
    context_bridge = ContextBridge()
    engine.rootContext().setContextProperty("contextBridge", context_bridge)

    qml_file: Path = qml_dir / "Main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    logger.info("Aplikasi dimulai.")
    _ = app.exec()


if __name__ == "__main__":
    run()
