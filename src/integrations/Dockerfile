FROM rocker/r-ver:4.0

RUN \
    apt-get update && \
    apt-get -y upgrade && \

    apt-get clean && \


    
COPY etl/ /opt/etl

CMD python /opt/etl/run.py


