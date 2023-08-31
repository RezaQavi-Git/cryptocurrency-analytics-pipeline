# cryptocurrency-analytics-pipeline


## Spark
link [https://github.com/brunocfnba/docker-spark-cluster]

```
version: '3'
services:
  spark-master:
    image: bitnami/spark:latest
    container_name: spark-master
    ports:
      - "8080:8080"  # Spark Master web UI
      - "7077:7077"  # Spark Master
    environment:
      - SPARK_MODE=master
    volumes:
      - ./data:/app  # Map your application code/data to /app in the container

  spark-worker:
    image: bitnami/spark:latest
    container_name: spark-worker
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077  # Use the name of the master container
    volumes:
      - ./data:/app  # Map your application code/data to /app in the container

```


CoinMarketcap

```
curl -H "X-CMC_PRO_API_KEY: "" 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?symbol=BTC' | json_pp
```


Wallex
```
'https://api.wallex.ir/v1/udf/history?symbol=USDTTMN&resolution=1&from=1693233309&to=1693233469'
```

