from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import *

import time
import logging
import os

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()
log.setLevel(logging.CRITICAL)

from minion.minioClient import MinIOClient
from utils import (
    Logger,
    generateFilePath,
    generateFileName,
    convertTimestampToDatetime,
    makeDirectory,
)
from configs import (
    CMC_API_CONFIG_CRYPTO_LIST,
    WALLEX_API_CONFIG_CRYPTO_LIST,
    CMC_RAW_DATA_SCHEMA,
    WALLEX_RAW_DATA_SCHEMA,
    FETCHED_DATA_FOLDER,
    AGG_DATA_FOLDER,
    PROCESSING_TIME_PERIOD,
    AGG_DATA_BUCKET,
    JOINED_DATA_BUCKET,
    JOINED_DATA_FOLDER,
    FILE_FORMAT,
)


def joinDataframes(cmcDataframe: DataFrame, wallexDataframe: DataFrame):
    joinedDataframe = cmcDataframe.join(
        wallexDataframe.select(col("price").alias("USDTTMNPrice"), col("timestamp")),
        on="timestamp",
        how="inner",
    )

    joinedDataframe = joinedDataframe.withColumn(
        "TMNPrice", (joinedDataframe.price * joinedDataframe.USDTTMNPrice)
    )
    joinedDataframe = joinedDataframe.withColumn(
        "TMNMarketCap", (joinedDataframe.marketCap * joinedDataframe.USDTTMNPrice)
    )
    return joinedDataframe


def timeFilterDataframe(dataframe: DataFrame, time: int):
    return dataframe.filter(
        (dataframe.timestamp < time)
        & (dataframe.timestamp > (time - PROCESSING_TIME_PERIOD))
    )


def processData(crypto: str, dataframe: DataFrame):
    # Aggregate Metrics
    # AVG Price
    # Highest Price, Lowest Price
    # Total Volume

    aggMetrics = dataframe.select(
        avg("price").alias("avgPrice"),
        max("price").alias("maxPrice"),
        min("price").alias("minPrice"),
        sum("volume").alias("totalVolume"),
        count("timestamp").alias("uniqueRecords"),
    )

    aggMetrics = aggMetrics.withColumn("symbol", lit(crypto))
    return aggMetrics
