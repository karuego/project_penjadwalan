from logging import Logger
from PySide6.QtCore import QObject, Slot, Signal


# Class untuk mengirim log ke QML
class LogBridge(QObject):
    logMessage: Signal = Signal(str)

    def __init__(self, logger: Logger, parent: QObject | None = None):
        super().__init__(parent)
        self._logger: Logger = logger

    def write(self, message: str) -> None:
        if message.strip():
            self.logMessage.emit(message.strip())

    def flush(self) -> None:
        pass

    @Slot(str)  # pyright: ignore[reportAny]
    def log(self, message: str) -> None:
        self._logger.info(message)
        self.logMessage.emit(message)

    @Slot(str)  # pyright: ignore[reportAny]
    def error(self, message: str) -> None:
        self._logger.error(message)
        self.logMessage.emit(message)
