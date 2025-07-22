# This Python file uses the following encoding: utf-8
import os
import sys
from pathlib import Path

# from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtCore import QObject, Signal, Slot

import application_rc

class Res:
    @staticmethod
    def get(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS) / relative_path  # jika dibundle
        return Path.cwd() / relative_path  # jika dijalankan langsung
        #return Path(__file__).resolve().parent / relative_path

class MainWindow(QObject):
    def __init__(self):
        super().__init__()
        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()

        # Set context properties
        self.engine.rootContext().setContextProperty("mainWindow", self)

        # Load QML
        qml_file = Res.get("qml/main.qml")
        self.engine.load(qml_file)

        if not self.engine.rootObjects():
            sys.exit(-1)

    @Slot(str)
    def handle_button_click(self, text):
        print(f"Button clicked with text: {text}")
        return f"Processed by Python: {text}"

    def run(self):
        return self.app.exec()


if __name__ == "__main__":
    # app = QGuiApplication(sys.argv)
    # engine = QQmlApplicationEngine()

    # qml_file = Path(__file__).resolve().parent / "qml/main.qml"
    # engine.load(qml_file)

    # if not engine.rootObjects():
    #     sys.exit(-1)

    # sys.exit(app.exec())

    window = MainWindow()
    sys.exit(window.run())
