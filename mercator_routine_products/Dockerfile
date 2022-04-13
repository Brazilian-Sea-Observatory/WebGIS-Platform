FROM continuumio/miniconda3:4.7.10

WORKDIR /home/geoserver/mercator_routine_products

COPY . .

RUN apt-get update --allow-releaseinfo-change -y && apt-get install pkg-config libgirepository1.0-dev libcairo2-dev build-essential -y
RUN apt-get install libcurl4-openssl-dev libssl-dev curl python2.7 python3-cairo-dev -y
RUN apt-get install cron -y 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install netCDF4

CMD /usr/sbin/cron -f
