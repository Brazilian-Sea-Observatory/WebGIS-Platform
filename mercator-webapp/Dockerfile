# estágio de compilação
FROM node:10.15.1-alpine as build-stage
RUN mkdir /app
WORKDIR /app
COPY package.json ./

#  RUN npm config rm proxy
# RUN npm config rm https-proxy
RUN npm config set registry http://registry.npmjs.org/
# RUN npm config set registry http://104.16.21.35/
RUN npm cache clean --force

# RUN cat /etc/resolv.conf; sleep 5
# RUN sudo echo "nameserver 8.8.8.8" >> /etc/resolv.conf
# RUN cat /etc/resolv.conf; sleep 5

# RUN ping -c 2 104.16.21.35
# RUN ping -c 2 registry.npmjs.org
RUN npm install node-sass --save

RUN npm install
# RUN npm install register-service-worker
COPY . .
RUN npm run build

# estágio de produção
FROM nginx:1.13.12-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY --from=build-stage /app/node_modules/vue/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf


RUN mkdir -p /root/certs/portal.brazilianseaobservatory.org/
COPY privkey.pem /root/certs/portal.brazilianseaobservatory.org/privkey.pem
COPY fullchain.pem /root/certs/portal.brazilianseaobservatory.org/fullchain.pem
RUN chmod -R 400 /root/certs/portal.brazilianseaobservatory.org/

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
