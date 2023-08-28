import time

from dataloader import CoinMarketCapAPIDataLoader, WallexAPIDataLoader
from configs import COINMARKETCAP_API_CONFIG, WALLEX_API_CONFIG


def main():
    coinMarketCap = CoinMarketCapAPIDataLoader(COINMARKETCAP_API_CONFIG)
    wallex = WallexAPIDataLoader(WALLEX_API_CONFIG)
    # while(True):

    # Fetch Request
    coinMarketCapResult = coinMarketCap.fetchAPIData(
        endPoint="v2/cryptocurrency/quotes/latest", queryParts={"symbol": "BTC"}
    )

    coinMarketCapResult = coinMarketCap.fetchAPIData(
        endPoint="v2/cryptocurrency/quotes/latest", queryParts={"symbol": "ETH"}
    )

    wallexResult = wallex.fetchAPIData(
        endPoint="v1/udf/history",
        queryParts={
            "symbol": "USDTTMN",
            "resolution": "1",
            "from": str(int(time.time() - 60)),
            "to": str(int(time.time())),
        },
    )
    # Handle result

    # Sleep
    return


main()
