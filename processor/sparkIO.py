from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import *

from enum import Enum

from process import timeFilterDataframe
from minion.minioClient import MinIOClient
from utils import (
    Logger,
    generateFilePath,
    generateFileName,
    convertTimestampToDatetime,
    makeDirectory,
)

from configs import (
    FETCHED_DATA_FOLDER,
    RAW_DATA_BUCKET,
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
)


class DataSource(Enum):
    LOCAL = "Local"
    MINIO = "Minio"


def sparkReadMinIO(spark: SparkSession, crypto: str):
    spark.conf.set("spark.hadoop.fs.s3a.endpoint", MINIO_ENDPOINT)
    spark.conf.set("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY)
    spark.conf.set("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY)

    minio_options = {"spark.hadoop.fs.s3a.path.style.access": False}

    df = (
        spark.read.format("json")
        .option("header", "false")
        .load(f"s3a://{RAW_DATA_BUCKET}/{crypto}", **minio_options)
    )

    return df


def readData(
    spark: SparkSession,
    crypto: str,
    schema: list,
    time: int,
    source: DataSource = DataSource.LOCAL,
):
    # MinIO Load Data
    # this section is in progress :(
    if source == DataSource.MINIO:
        df = sparkReadMinIO(spark=spark, crypto=crypto)
    else:
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
        dataframe = readData(
            spark=spark,
            crypto=crypto,
            schema=schema,
            time=time,
            source=DataSource.LOCAL,
        )
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
        Logger().getLogger().error(f"Write to file failed, error {e}")
