from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import *

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()
log.setLevel(logging.WARNING)



from utils import Logger, generateFilePath
from configs import (
    CMC_API_CONFIG_CRYPTO_LIST,
    WALLEX_API_CONFIG_CRYPTO_LIST,
    CMC_RAW_DATA_SCHEMA,
    WALLEX_RAW_DATA_SCHEMA,
    FETCHED_DATA_FOLDER,
    AGG_DATA_FOLDER
)


def processData(spark: SparkSession, dataframe: DataFrame):

    # TimeBased Filter 

    # Aggregate Metrics 
        # AVG Price
        # Highest Price, Lowest Price
        # Total Volume 


    return


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


def loadRawData(spark: SparkSession, crypto: str, schema: list):
    # MinIO Load Data
    # this section is in progress :(

    # Load Local Data
    df = spark.read.csv(path=generateFilePath(folderPath=FETCHED_DATA_FOLDER, fileName=crypto))
    df = df.toDF(*schema)
    return df


def main():
    # Create spark session
    spark = createSparkSession(appName="ProccessFetchedRawData")
    
    # Load
    cmcDataframes = Dict()
    # CMC
    for crypto in CMC_API_CONFIG_CRYPTO_LIST:
        dataframe = loadRawData(spark=spark, crypto=crypto, schema=CMC_RAW_DATA_SCHEMA)
        cmcDataframes.update({crypto: dataframe})

    # Wallex 
    wallexDataframes = Dict()
    for crypto in WALLEX_API_CONFIG_CRYPTO_LIST:
        dataframe = loadRawData(spark=spark, crypto=crypto, schema=WALLEX_RAW_DATA_SCHEMA)
        wallexDataframes.update({crypto: dataframe})

    # Transform
    

    # Store


    return


main()