import os
from dotenv import load_dotenv

load_dotenv()
 

# General Configurations 

SLEEP_TIME = 60
FETCHED_DATA_FOLDER = './fetched/'

HTTP_CALL_MAX_RETRIES = 4
HTTP_CALL_TIMEOUT = 10
HTTP_CALL_DELAY = 5


# CMC Configurations
 
CMC_API_CONFIG = {
    "url": "https://pro-api.coinmarketcap.com/",
    "headerAuthKey": "X-CMC_PRO_API_KEY",
    "token": os.environ.get("CMC_TOKEN"),
}

CMC_API_CONFIG_CRYPTO_LIST = ['ETH', 'BTC']

CMC_TIMESTAMP_STR_PATTERN = "%Y-%m-%dT%H:%M:%S.%fZ"

# Wallex Configurations 

WALLEX_API_CONFIG = {
    "url": "https://api.wallex.ir/",
    "headerAuthKey": "X-API-Key",
    "token": os.environ.get("WALLEX_TOKEN"),
}

WALLEX_API_CONFIG_CRYPTO_LIST = ['USDTTMN']

# MinOI Configurations 
MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')

RAW_DATA_BUCKET = "test-raw-data"
AGG_DATA_BUCKET = "test-raw-data"

