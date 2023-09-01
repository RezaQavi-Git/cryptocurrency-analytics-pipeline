import requests, csv, time
import urllib.parse
from datetime import datetime

from utils import Logger, generateFilePath
from minion.minioClient import MinIOClient
from configs import (
    CMC_TIMESTAMP_STR_PATTERN,
    HTTP_CALL_MAX_RETRIES,
    HTTP_CALL_TIMEOUT,
    HTTP_CALL_DELAY,
    RAW_DATA_BUCKET,
    FETCHED_DATA_FOLDER,
    FILE_FORMAT
)


class APIDataProvider:
    def __init__(self, config) -> None:
        self.config = config
        pass

    def generateQuery(self, queryParts: dict):
        query_string = urllib.parse.urlencode(queryParts)
        return "?" + query_string

    def httpRequest(self, apiUrl):
        headers = {
            self.config["headerAuthKey"]: self.config["token"],
        }
        for retry in range(HTTP_CALL_MAX_RETRIES):
            try:
                session = requests.Session()
                response = session.get(
                    apiUrl, headers=headers, timeout=HTTP_CALL_TIMEOUT
                )
                response.raise_for_status()
                if response.status_code == 200:
                    return response.json()
                else:
                    return None
            except Exception as e:
                Logger().getLogger().warning(
                    f"Request failed. Retrying ({retry + 1}/{HTTP_CALL_MAX_RETRIES})..."
                )
                time.sleep(HTTP_CALL_DELAY)

        raise Exception("Max retries exceeded")

    def fetchAPIData(self, endPoint: str, queryParts: dict):
        apiUrl = (
            self.config["url"] + endPoint + self.generateQuery(queryParts=queryParts)
        )
        response = self.httpRequest(apiUrl=apiUrl)
        return response

    def parseAPIResponse(self, response: str, symbol: str):
        return

    def storeParsedResult(self, data: dict, filename: str, time: int):
        minioClient = MinIOClient()

        if minioClient.checkBucketExists(bucket=RAW_DATA_BUCKET):
            minioClient.putObject(
                bucket=RAW_DATA_BUCKET,
                data=data,
                folderName=filename,
                fileName=str(time),
            )

        with open(
            generateFilePath(folderPath=FETCHED_DATA_FOLDER, fileName=filename) + FILE_FORMAT,
            mode="a",
            newline="",
        ) as file:
            writer = csv.writer(file)
            writer.writerow([str(time)] + list(data.values()))
            file.close()
        Logger().getLogger().info(f"Data successfully wrote to {filename}")


class CoinMarketCapAPIDataProvider(APIDataProvider):
    def __init__(self, config) -> None:
        super().__init__(config)

    def convertTimestamp(self, strTimestamp: str, pattern: str):
        datetimeObj = datetime.strptime(strTimestamp, pattern)
        timestamp = datetimeObj.timestamp()

        return str(int(timestamp))

    def parseAPIResponse(self, response: str, symbol: str):
        # print("CMC", response)
        responseQuote = response["data"][symbol][0]["quote"]["USD"]
        return {
            "timestamp": self.convertTimestamp(
                strTimestamp=responseQuote["last_updated"],
                pattern=CMC_TIMESTAMP_STR_PATTERN,
            ),
            "symbol": symbol,
            "name": response["data"][symbol][0]["name"],
            "price": responseQuote["price"],
            "volume": responseQuote["volume_24h"],
            "market_cap": responseQuote["market_cap"],
        }


class WallexAPIDataProvider(APIDataProvider):
    def __init__(self, config) -> None:
        super().__init__(config)

    def parseAPIResponse(self, response: str, symbol: str):
        # print("Wallex", response)
        return {
            "timestamp": response["t"][0],
            "symbol": symbol,
            "price": response["c"][0],
            "volume": response["v"][0],
        }
