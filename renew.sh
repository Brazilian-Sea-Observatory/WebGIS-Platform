#!/bin/bash

docker-compose stop frontend

certbot renew

cp /etc/letsencrypt/live/portal.brazilianseaobservatory.org/*.pem /home/maretec/mercator/mercator-webapp/

docker-compose build --no-cache frontend
docker-compose up -d frontend
