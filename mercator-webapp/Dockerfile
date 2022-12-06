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

# estágio de produção
#FROM nginx:1.13.12-alpine as production-stage

FROM nginx:stable as production-stage

ARG CERTBOT_EMAIL=humberto.ibanez@gmail.com
ARG DOMAIN_LIST=brasea.org

#COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY --from=build-stage /app/node_modules/vue/dist /usr/share/nginx/html
#RUN mkdir /usr/share/nginx/html/.well-known;mkdir /usr/share/nginx/html/.well-known/acme-challenge
COPY nginx.conf /etc/nginx/nginx.conf
# Estou comentando os próximos 4 comandos porque a ligação dos .pem que são gerados no docker certbot com o frontend passará a ser feita pelos volumes dos respectivos serviços: certbot e frontend
#RUN mkdir -p /root/certs/brasea.org/
#COPY privkey.pem /root/certs/brasea.org/privkey.pem
#COPY fullchain.pem /root/certs/brasea.org/fullchain.pem
#RUN chmod -R 400 /root/certs/brasea.org/

RUN  apt-get update \
      && apt-get install -y cron certbot python3-certbot-nginx bash wget \
      && certbot certonly --standalone --agree-tos -m "${CERTBOT_EMAIL}" -n -d ${DOMAIN_LIST} \
      && rm -rf /var/lib/apt/lists/* \
      && echo "PATH=$PATH" > /etc/cron.d/certbot-renew  \
      && echo "@monthly certbot renew --nginx >> /var/log/cron.log 2>&1" >>/etc/cron.d/certbot-renew \
      && crontab /etc/cron.d/certbot-renew

VOLUME /etc/letsencrypt

CMD [ "sh", "-c", "cron && nginx -g 'daemon off;'" ]


EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
