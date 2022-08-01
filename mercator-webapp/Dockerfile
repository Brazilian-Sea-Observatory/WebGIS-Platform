# estágio de compilação
FROM node:10.15.1-alpine as build-stage
RUN mkdir /app
WORKDIR /app
COPY package.json ./
RUN npm install node-sass --save
RUN npm install
COPY . .
RUN npm run build

# estágio de produção
FROM nginx:1.13.12-alpine as production-stage
#COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY --from=build-stage /app/node_modules/vue/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /root/certs/portal.brazilianseaobservatory.org/
COPY privkey.pem /root/certs/portal.brazilianseaobservatory.org/privkey.pem
COPY fullchain.pem /root/certs/portal.brazilianseaobservatory.org/fullchain.pem
RUN chmod -R 400 /root/certs/portal.brazilianseaobservatory.org/

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
