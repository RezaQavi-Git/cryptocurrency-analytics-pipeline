import time

from dataProvider import CoinMarketCapAPIDataProvider, WallexAPIDataProvider
from configs import (
    CMC_API_CONFIG,
    WALLEX_API_CONFIG,
    CMC_API_CONFIG_CRYPTO_LIST,
    WALLEX_API_CONFIG_CRYPTO_LIST,
)


def main():
    coinMarketCap = CoinMarketCapAPIDataProvider(CMC_API_CONFIG)
    wallex = WallexAPIDataProvider(WALLEX_API_CONFIG)
    # while(True):

    # Fetch Request

    # CoinMarketCap
    for crypto in CMC_API_CONFIG_CRYPTO_LIST:
        CMCResponse = coinMarketCap.fetchAPIData(
            endPoint="v2/cryptocurrency/quotes/latest", queryParts={"symbol": crypto}
        )
        print(coinMarketCap.parseAPIResponse(response=CMCResponse, symbol=crypto))

    # Wallex
    for crypto in WALLEX_API_CONFIG_CRYPTO_LIST:
        wallexResponse = wallex.fetchAPIData(
            endPoint="v1/udf/history",
            queryParts={
                "symbol": crypto,
                "resolution": "1",
                "from": str(int(time.time() - 60)),
                "to": str(int(time.time())),
            },
        )
        print(wallex.parseAPIResponse(response=wallexResponse, symbol=crypto))
    # Handle result

    # Sleep
    return


main()
