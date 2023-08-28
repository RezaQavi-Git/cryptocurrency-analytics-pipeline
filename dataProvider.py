import requests, json
import urllib.parse
from datetime import datetime

from configs import CMC_TIMESTAMP_STR_PATTERN


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
        response = requests.get(apiUrl, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetchAPIData(self, endPoint: str, queryParts: dict):
        apiUrl = (
            self.config["url"] + endPoint + self.generateQuery(queryParts=queryParts)
        )
        response = self.httpRequest(apiUrl=apiUrl)
        return response

    def parseAPIResponse(self, response: str, symbol: str):
        return


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
