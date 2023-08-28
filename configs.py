import os
from dotenv import load_dotenv

load_dotenv()



COINMARKETCAP_API_CONFIG = {
    'url': 'https://pro-api.coinmarketcap.com/',
    'headerAuthKey': 'X-CMC_PRO_API_KEY',
    'token': os.environ.get('COINMARKETCAP_TOKEN'),
    
}

WALLEX_API_CONFIG = {
    'url': 'https://api.wallex.ir/',
    'headerAuthKey': 'X-API-Key',
    'token': os.environ.get('WALLEX_TOKEN'),

}

