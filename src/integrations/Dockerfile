FROM python:3.9-slim

RUN \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /

RUN \
    pip install --upgrade pip && \
    pip install -r requirements.txt
    
COPY etl/ /opt/etl

CMD python /opt/etl/run.py
