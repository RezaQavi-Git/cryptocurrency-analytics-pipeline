# Cryptocurrency Analytics Pipeline

This Python-based project cryptocurrency analytics pipeline, consisting of the following major components:

## Part 1: Data Collection and Storage

In the first part of this project, we've developed a web crawler that utilizes HTTP requests to access data from a free cryptocurrency API. The fetched data is then parsed based on the API provider's response schema. The processed data is stored in two locations:

- **MinIO:** A powerful object storage service for secure and scalable data storage.
- **Local CSV Files:** Data is also persisted in local CSV files for easy access.

## Part 2: Data Processing with Apache Spark (PySpark)

The second part of this project involves data processing using Apache Spark, specifically the PySpark library. This phase consists of two primary tasks:

### Task 1: Aggregate Metrics Calculation

We perform essential calculations on the raw datasets. Key metrics such as average price, volume, market capitalization, and etc.

### Task 2: Dataset Joining and Conversion
In this phase, we combine datasets from CoinMarketCap (CMC) with those from Wallex. The result is a unified dataset that includes pricing information from CoinMarketCap in USD and converts it to TMN (the Iran Toman currency). Furthermore


## Used APIs 

### CoinMarketcap
From the CMC API documentation I found this API provide me necessary data witch need in this project.

example:
```bash
curl -H "X-CMC_PRO_API_KEY: "" 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?symbol=BTC'
```

### Wallex
From the Wallex exchange API documentation I found this API provide me necessary data witch need in this project.

example:
```bash
curl 'https://api.wallex.ir/v1/udf/history?symbol=USDTTMN&resolution=1&from=1693233309&to=1693233469'
```

## How to Run

This project consists of two major parts, each of which should be run separately:

### 1. Crawler

The Crawler is responsible for fetching data from the APIs mentioned earlier and storing it in local CSV files and MinIO. To set up MinIO, refer to the `minio` folder in the repository.

```bash
git clone https://github.com/RezaQavi-Git/cryptocurrency-analytics-pipeline.git
cd cryptocurrency-analytics-pipeline/
export PYTHONPATH=$PWD
python3 -m venv {venv_name}
source {venv_name}/bin/activate

pip install -r requirements.txt

python3 crawler/main.py
```


### 2. Processor
The Processor uses the data obtained from the Crawler and performs data processing using PySpark. It also provides aggregated results, which are stored in local CSV files and MinIO.

```bash
spark-submit processor/dataProcessing.py
```
This code should be scheduled to run hourly.

