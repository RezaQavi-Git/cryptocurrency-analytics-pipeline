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
from utils import Logger, generateFilePath, generateFileName, convertTimestampToDatetime, makeDirectory
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


def readData(spark: SparkSession, crypto: str, schema: list, time: int):
    # MinIO Load Data
    # this section is in progress :(

    # Load Local Data
    df = spark.read.csv(
        path=generateFilePath(folderPath=FETCHED_DATA_FOLDER, fileName=crypto)
    )
    df = df.toDF(*schema)

    # TimeBased Filter
    df = timeFilterDataframe(dataframe=df, time=time)
    return df


def loadRawData(spark: SparkSession, cryptoList: list, schema: list, time: int):
    dataframes = {}
    for crypto in cryptoList:
        dataframe = readData(spark=spark, crypto=crypto, schema=schema, time=time)
        dataframes.update({crypto: dataframe})

    return dataframes


def storeProcessedData(
    crypto: str, dataframe: DataFrame, bucket: str, folder: str, time: int
):
    dataframeToJson = dataframe.toJSON().collect()
    minioClient = MinIOClient()

    if minioClient.checkBucketExists(bucket=bucket):
        minioClient.putDataframeObject(
            bucket=bucket,
            jsonDataframe=dataframeToJson,
            folderName=crypto,
            fileName=convertTimestampToDatetime(timestamp=time),
        )

    outputPath = generateFileName(
        folderPath=folder,
        fileName=f"{crypto}_{convertTimestampToDatetime(timestamp=time)}",
    )

    try:
        makeDirectory(outputPath)
        dataframe.write.csv(outputPath, header=True, mode="overwrite")
        Logger().getLogger().info(f"Data successfully wrote to {outputPath}")
    except Exception as e:
        Logger().getLogger().error(f'Write to file failed, error {e}')

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
        # time=now,
        time=1693304521,
    )
    # Wallex
    wallexDataframes = loadRawData(
        spark=spark,
        cryptoList=WALLEX_API_CONFIG_CRYPTO_LIST,
        schema=WALLEX_RAW_DATA_SCHEMA,
        # time=now,
        time=1693304521,
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
