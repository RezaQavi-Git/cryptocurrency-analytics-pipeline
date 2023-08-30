import time

from dataProvider import CoinMarketCapAPIDataProvider, WallexAPIDataProvider

from utils import Logger
from configs import (
    SLEEP_TIME,
    CMC_API_CONFIG,
    WALLEX_API_CONFIG,
    CMC_API_CONFIG_CRYPTO_LIST,
    WALLEX_API_CONFIG_CRYPTO_LIST,
)


def main():
    coinMarketCap = CoinMarketCapAPIDataProvider(CMC_API_CONFIG)
    wallex = WallexAPIDataProvider(WALLEX_API_CONFIG)
    while True:
        now = int(time.time())
        # CoinMarketCap
        for crypto in CMC_API_CONFIG_CRYPTO_LIST:
            try:
                CMCResponse = coinMarketCap.fetchAPIData(
                    endPoint="v2/cryptocurrency/quotes/latest",
                    queryParts={"symbol": crypto},
                )
                cmcResult = coinMarketCap.parseAPIResponse(
                    response=CMCResponse, symbol=crypto
                )

                # CMC fetched data file row format
                # (now timestamp),(last updated timestamp),(symbol),(name),(price),(volume),(marketCap)
                coinMarketCap.storeParsedResult(
                    data=cmcResult,
                    filename=crypto,
                    time=now,
                )
            except Exception as e:
                Logger().getLogger().warning(e)

        # Wallex
        timestamp = (now // 60) * 60
        for crypto in WALLEX_API_CONFIG_CRYPTO_LIST:
            try:
                wallexResponse = wallex.fetchAPIData(
                    endPoint="v1/udf/history",
                    queryParts={
                        "symbol": crypto,
                        "resolution": "1",
                        "from": str(timestamp - SLEEP_TIME),
                        "to": str(timestamp + SLEEP_TIME),
                    },
                )
                wallexResult = wallex.parseAPIResponse(
                    response=wallexResponse, symbol=crypto
                )

                # Wallex fetched data file row format
                # (now timestamp),(last updated timestamp),(symbol),(price),(volume)
                wallex.storeParsedResult(
                    data=wallexResult,
                    filename=crypto,
                    time=now,
                )
            except Exception as e:
                Logger().getLogger().warning(e)

        # Sleep
        time.sleep(SLEEP_TIME)


main()
