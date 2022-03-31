FROM node:alpine AS build-stage
WORKDIR /build
COPY . .
RUN npm install && npm run build


FROM keymetrics/pm2:latest-alpine
RUN apk add --update python python-dev py-pip build-base
# Bundle APP files
COPY --from=build-stage /build/dist src/
COPY ./wind-data/ /wind-data
COPY cert.pem .
COPY key.pem .
COPY package.json .
COPY ecosystem.config.js .

# Install app dependencies
ENV NPM_CONFIG_LOGLEVEL warn
RUN npm install --production

# Expose the listening port of your app
EXPOSE 8081
EXPOSE 443

# Show current folder structure in logs
RUN ls -al -R

CMD [ "pm2-runtime", "start", "ecosystem.config.js" ]
