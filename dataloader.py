import requests
import urllib.parse


class APIDataLoader:
    def __init__(self, config) -> None:
        self.config = config
        pass

    def fetchAPIData(self, endPoint: str, queryParts: dict):
        apiUrl = (
            self.config["url"] + endPoint + self.generateQuery(queryParts=queryParts)
        )
        response = self.httpRequest(apiUrl=apiUrl)
        print(response)
        return

    def generateQuery(self, queryParts: dict):
        query_string = urllib.parse.urlencode(queryParts)
        return "?" + query_string

    def httpRequest(self, apiUrl):
        headers = {
            self.config['headerAuthKey']: self.config['token'],
        }
        response = requests.get(apiUrl, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None


class CoinMarketCapAPIDataLoader(APIDataLoader):
    def __init__(self, config) -> None:
        super().__init__(config)


class WallexAPIDataLoader(APIDataLoader):
    def __init__(self, config) -> None:
        super().__init__(config)
