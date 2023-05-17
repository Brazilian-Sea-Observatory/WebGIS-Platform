# estágio de compilação
FROM node:10.15.1-alpine as build-stage
RUN mkdir /app
WORKDIR /app
COPY package.json ./
RUN npm cache verify
RUN rm -rf node_modules
RUN rm -rf package-lock.json
RUN npm install node-sass --save
RUN npm install
COPY . .
RUN npm run build

COPY /app/node_modules/vue/dist ./letsencrypt-docker-compose/html

# estágio de produção
#FROM nginx:1.13.12-alpine as production-stage

#16mai2023 para funcionar junto com letsencrypt-docker-compose
#16mai2023 FROM nginx:stable as production-stage

#16mai2023 ARG CERTBOT_EMAIL=humberto.ibanez@gmail.com
#16mai2023 ARG DOMAIN_LIST=brasea.org

#COPY --from=build-stage /app/dist /usr/share/nginx/html
#16mai2023 COPY --from=build-stage /app/node_modules/vue/dist /usr/share/nginx/html
#16mai2023 ERROR: failed to solve: circular dependency detected on stage: build-stage COPY --from=build-stage /app/node_modules/vue/dist ./letsencrypt-docker-compose/html
#16mai2023 No nginx de letsencrypt-docker-compose/docker-compose.yml tem o volume ./html:/var/www/html:ro
#RUN mkdir /usr/share/nginx/html/.well-known;mkdir /usr/share/nginx/html/.well-known/acme-challenge
#16mai2023 COPY nginx.conf /etc/nginx/nginx.conf
# Estou comentando os próximos 4 comandos porque a ligação dos .pem que são gerados no docker certbot com o frontend passará a ser feita pelos volumes dos respectivos serviços: certbot e frontend
#RUN mkdir -p /root/certs/brasea.org/
#COPY privkey.pem /root/certs/brasea.org/privkey.pem
#COPY fullchain.pem /root/certs/brasea.org/fullchain.pem
#RUN chmod -R 400 /root/certs/brasea.org/

#16mai2023 RUN  apt-get update \
#16mai2023       && apt-get install -y cron certbot python3-certbot-nginx bash wget \
#16mai2023       && certbot certonly --standalone --agree-tos -m "${CERTBOT_EMAIL}" -n -d ${DOMAIN_LIST} \
#16mai2023       && rm -rf /var/lib/apt/lists/* \
#16mai2023       && echo "PATH=$PATH" > /etc/cron.d/certbot-renew  \
#16mai2023       && echo "@monthly certbot renew --nginx >> /var/log/cron.log 2>&1" >>/etc/cron.d/certbot-renew \
#16mai2023       && crontab /etc/cron.d/certbot-renew

#16mai2023 VOLUME /etc/letsencrypt

#16mai2023 CMD [ "sh", "-c", "cron && nginx -g 'daemon off;'" ]


#16mai2023 EXPOSE 80
#16mai2023 EXPOSE 443

#16mai2023 CMD ["nginx", "-g", "daemon off;"]
