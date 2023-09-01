# Crawler

The Crawler is responsible for fetching data from the APIs mentioned earlier and storing it in local CSV files and MinIO. To set up MinIO, refer to the `minion` folder in the repository.

## How To Run
1. Local: To run this project locally, as you can see in README.md [link](../README.md) file in this project, use below command: 

```bash
spark-submit processor/dataProcessing.py
```

But if you want run it as a docker container, follow below steps:

```bash

docker build -t processor -f Dockerfile.processor .
docker-compose -f processor.yaml up
```

1. Also need to run minio docker-compose file [link](../minion/minio.yaml).
2. Also need to run spark-cluster docker-compose file [link](https://github.com/RezaQavi-Git/spark-docker-cluster#readme)