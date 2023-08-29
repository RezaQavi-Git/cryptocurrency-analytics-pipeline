import os
from dotenv import load_dotenv

load_dotenv()

SLEEP_TIME = 60
FETCHED_DATA_FOLDER = './fetched/'

CMC_API_CONFIG = {
    "url": "https://pro-api.coinmarketcap.com/",
    "headerAuthKey": "X-CMC_PRO_API_KEY",
    "token": os.environ.get("CMC_TOKEN"),
}

CMC_API_CONFIG_CRYPTO_LIST = ['ETH', 'BTC']

CMC_TIMESTAMP_STR_PATTERN = "%Y-%m-%dT%H:%M:%S.%fZ"

WALLEX_API_CONFIG = {
    "url": "https://api.wallex.ir/",
    "headerAuthKey": "X-API-Key",
    "token": os.environ.get("WALLEX_TOKEN"),
}

WALLEX_API_CONFIG_CRYPTO_LIST = ['USDTTMN']