from logging import Logger, DEBUG, getLogger, StreamHandler, Formatter

name = "jadwal"

logger: Logger = getLogger(name)
logger.setLevel(DEBUG)

if not logger.hasHandlers():
    handler = StreamHandler()
    formatter = Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

@staticmethod
def debug(msg: str) -> None:
    logger.debug(msg)

@staticmethod
def info(msg: str) -> None:
    logger.info(msg)

@staticmethod
def warning(msg: str) -> None:
    logger.warning(msg)

@staticmethod
def error(msg: str) -> None:
    logger.error(msg)
