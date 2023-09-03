# Processor

The Processor uses the data obtained from the Crawler and performs data processing using PySpark. It also provides aggregated results, which are stored in local CSV files and MinIO.

## How To Run
1. Local: To run this project locally, as you can see in README.md [link](../README.md) file in this project, use below command: 

```bash
git clone https://github.com/RezaQavi-Git/cryptocurrency-analytics-pipeline.git
cd cryptocurrency-analytics-pipeline/
export PYTHONPATH=$PWD
python3 -m venv {venv_name}
source {venv_name}/bin/activate

pip install -r requirements.txt

python3 crawler/main.py
```

But if you want run it as a docker container, follow below steps:

```bash
docker network create application_network
docker build -t crawler -f Dockerfile.crawler
docker-compose -f crawler.yaml up
```

also need to run minio docker-compose file [link](../minion/minio.yaml).
