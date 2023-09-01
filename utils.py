import logging
from datetime import datetime

from configs import FETCHED_DATA_FOLDER


logging.basicConfig(level=logging.DEBUG)


class Logger:
    def __init__(self) -> None:
        self.logger = logging.getLogger("CMC-Wallex Data Crawler")
        self.logger.setLevel(logging.DEBUG)
        pass

    def getLogger(self) -> logging:
        return self.logger


def generateFilePath(folderPath: str, fileName: str):
    return folderPath + fileName


def convertTimestampToDatetime(timestamp: int):
    return str(
        datetime.utcfromtimestamp(timestamp)
        .replace(second=0, microsecond=0, minute=0)
        .strftime("%Y-%m-%dT%H-%M-%S")
    )
