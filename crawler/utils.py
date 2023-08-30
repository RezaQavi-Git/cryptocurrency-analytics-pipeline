import logging

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
    return folderPath + fileName + ".csv"
