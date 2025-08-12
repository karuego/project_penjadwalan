# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

# from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtCore import QObject, Signal, Slot


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # Tentukan path ke direktori yang berisi modul QML Anda
    qml_dir = Path(__file__).resolve().parent / "qml"

    # Beritahu engine untuk mencari modul di dalam direktori 'qml/'
    engine.addImportPath(str(qml_dir))

    # Muat file Main.qml dari direktori tersebut
    qml_file = qml_dir / "Main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
