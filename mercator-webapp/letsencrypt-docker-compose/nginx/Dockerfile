# estágio de compilação (copiado do Dockerfile de mercator-webapp)
#FROM node:10.15.1-alpine as build-stage
#https://stackoverflow.com/a/62064450
FROM node:latest as build-stage
RUN mkdir /app
WORKDIR /app
COPY package.json ./
RUN npm cache verify
RUN rm -rf node_modules
RUN rm -rf package-lock.json
RUN export PYTHON=python2
#npm install node-sass --save https://dev.to/ccreusat/migrating-from-node-sass-to-sass-dart-sass-with-npm-3g3c
RUN npm install --save-dev sass 
RUN npm i -D sass
RUN npm install
COPY . .
#https://stackoverflow.com/a/71262331
ENV NODE_ENV=production
RUN npm run build

# estágio de produção

FROM nginx:1.23-alpine as production-stage

RUN apk add --no-cache openssl jq

WORKDIR /letsencrypt-docker-compose

COPY config-nginx.sh start-nginx.sh ./
RUN chmod +x config-nginx.sh start-nginx.sh

COPY --from=build-stage /app/node_modules/vue/dist ./html/

EXPOSE 80

CMD ["/letsencrypt-docker-compose/start-nginx.sh"]
