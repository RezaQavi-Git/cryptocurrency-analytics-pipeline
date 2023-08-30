from minio import Minio
import json
from io import BytesIO

from configs import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
from utils import Logger


class MinIOClient:
    def __init__(self) -> None:
        try:
            self.minioClient = Minio(
                endpoint=MINIO_ENDPOINT,
                access_key=MINIO_ACCESS_KEY,
                secret_key=MINIO_SECRET_KEY,
                secure=False,  # Set to True if you are using HTTPS
            )
        except Exception as e:
            Logger().getLogger().error(f"Create MinIO Client Error: {e}")

    def getMinioClient(self):
        return self.minioClient

    def checkBucketExists(self, bucket):
        # Check if the folder exists, create it if not
        if not self.minioClient.bucket_exists(bucket):
            self.minioClient.make_bucket(bucket)

        return True        

    def putObject(self, bucket: str, data: dict, folderName: str, fileName: str):
        data_json = json.dumps(data).encode("utf-8")
        # Create a BytesIO object
        data_stream = BytesIO(data_json)

        object_name = f"{folderName}/{fileName}.json"
        try:
            self.minioClient.put_object(
                bucket_name=bucket,
                object_name=object_name,
                data=data_stream,
                length=len(data_json),
                content_type="application/json",
            )

            Logger().getLogger().info(f"MinIO Upload Successful: {object_name}")

        except Exception as e:
            Logger().getLogger().error(f"MinIO Upload error: {e}")
