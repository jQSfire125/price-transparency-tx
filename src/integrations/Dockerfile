FROM python:3.8-buster

RUN \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install python3-pandas \
    apt-get clean && \


    
COPY etl/ /opt/etl

CMD python /opt/etl/run.py


