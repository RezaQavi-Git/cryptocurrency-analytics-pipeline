from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import *

import time
import logging
import os

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()
log.setLevel(logging.CRITICAL)


from sparkIO import loadRawData, storeProcessedData
from process import processData, joinDataframes

from utils import (
    Logger,
)
from configs import (
    CMC_API_CONFIG_CRYPTO_LIST,
    WALLEX_API_CONFIG_CRYPTO_LIST,
    CMC_RAW_DATA_SCHEMA,
    WALLEX_RAW_DATA_SCHEMA,
    AGG_DATA_FOLDER,
    AGG_DATA_BUCKET,
    JOINED_DATA_BUCKET,
    JOINED_DATA_FOLDER,
)


def createSparkSession(appName: str) -> SparkSession:
    return (
        SparkSession.builder.appName(appName)
        .master("local[*]")
        .config("spark.executor.memory", "4g")
        .config("spark.driver.memory", "2g")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.default.parallelism", "4")
        .getOrCreate()
    )


def main():
    # Create spark session
    spark = createSparkSession(appName="ProcessFetchedRawData")

    now = int(time.time())
    # Load
    dataframes = {}
    # CMC
    cmcDataframes = loadRawData(
        spark=spark,
        cryptoList=CMC_API_CONFIG_CRYPTO_LIST,
        schema=CMC_RAW_DATA_SCHEMA,
        time=now,
    )
    # Wallex
    wallexDataframes = loadRawData(
        spark=spark,
        cryptoList=WALLEX_API_CONFIG_CRYPTO_LIST,
        schema=WALLEX_RAW_DATA_SCHEMA,
        time=now,
    )

    dataframes.update(cmcDataframes)
    dataframes.update(wallexDataframes)

    # Transform
    aggregateData = []
    for crypto, dataframe in dataframes.items():
        Logger().getLogger().info(f"Start Processing {crypto}")
        aggregateData.append(
            {"crypto": crypto, "data": processData(crypto=crypto, dataframe=dataframe)}
        )

    # Join CMC with Wallex
    joinedData = []
    for crypto, dataframe in cmcDataframes.items():
        Logger().getLogger().info(
            f"Start Joining CMC {crypto} over Wallex Dataframe USDTTMN"
        )
        joinedData.append(
            {
                "crypto": crypto,
                "data": joinDataframes(
                    cmcDataframe=dataframe, wallexDataframe=dataframes["USDTTMN"]
                ),
            }
        )

    # Store
    # Aggregated Data
    for item in aggregateData:
        storeProcessedData(
            crypto=item["crypto"],
            dataframe=item["data"],
            bucket=AGG_DATA_BUCKET,
            folder=AGG_DATA_FOLDER,
            time=now,
        )

    # Joined Data
    for item in joinedData:
        storeProcessedData(
            crypto=item["crypto"],
            dataframe=item["data"],
            bucket=JOINED_DATA_BUCKET,
            folder=JOINED_DATA_FOLDER,
            time=now,
        )

    return


main()
