# Instalação da WebGIS-Platform

A WebGIS-Platform emprega a seguinte Stack:

- Vue.js (com Typescript)
- Vuex
- Vuetify
- Scss
- Leaflet
- Leaflet Velocity
- Docker + Docker Compose
- Node.js
- GeoServer
- PostgreSQL
- Strapi.js


1 - Clonar Projeto
git clone https://github.com/Brazilian-Sea-Observatory/WebGIS-Platform.git

1.1 - Ir para o branch mais atual: buildingAAMMx, AA=ano, MM=mês, x=a,b,c,...
git checkout building2206b

2 - Instalar Node JS

```bash
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs
```

3 - Instalar Docker

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install \
  apt-transport-https \
  ca-certificates \
  curl \
  gcc \
  g++ \
  make \
  gnupg \
  lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

```

4 - Instalar Docker-Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

5 - Instalar as libs JS e construir a ferramenta para simulações de espalhamento de óleo (Oil Spill tool)

```bash
cd ./mercator-server
npm install
TODO: O npm install está emitindo vários avisos de deprecated e vulnerabilidades. Isto se dá porque os packege.json estão com versões de bibliotecas js antigas. Por enquanto não vamos alterar (ou atualizar) essas bibliotecas, pois a prioridade é manter o WebGIS original para chegar em uma versão operacional. Depois procederemos paulatinamente as atualizações.

npm run build
# export SPREAD_OIL_PATH=<caminho para a ferramenta do modelo lagrangiano>
# como por exemplo: 
export SPREAD_OIL_PATH=/home/maretec/WebGIS-Platform/Lagrangian_Global/BSO
npm start

cd .. (retorna para WebGIS-Platform)
```

Toda a aplicação, exceto a parte que comunica com a ferramenta do modelo de espalhamento de óleo roda dentro de containers Docker e estão configuradas no arquivo: **WebGIS-Platform/docker-compose.yml**.

É possível levantar os serviços individualmente (recomendado) ou todos os serviços de uma única vez com o comando: `docker-compose up -d`.

Para subir individualmente, execute o comando: docker-compose up -d "service"
em que "service" é um dos services configurados em WebGIS-Platform/docker-compose.yml

**Atenção:** A partir daqui os comandos foram executados com permissão de administrador: `sudo`

6 - Subir Backend

```bash
sudo /usr/local/bin/docker-compose up -d backend
```

7 - Instalar PM2

```bash
Verificar se o branch trouxe o link simbólico. Caso esteja faltando, criá-lo com o comando ln
cd mercator-server/src
WebGIS-Platform/mercator-server/src$ ln -s ../dist/index.js

cd ..

WebGIS-Platform/mercator-server$ sudo npm install -g pm2
WebGIS-Platform/mercator-server$ sudo pm2 start ecosystem.config.js

cd .. (retorna para WebGIS-Platform)
```

8 - Subir Frontend

```bash
sudo /usr/local/bin/docker-compose up -d frontend
```

9 - Subir Scripts
sudo /usr/local/bin/docker-compose up -d scripts

10 - Subir Base de dados

10.1 - Subir PostgreSQL/PostGIS

Os "services" postgres e rundeck estão definidos em WebGIS-Platform/rundeck/docker-compose.yml

cd rundeck

sudo /usr/local/bin/docker-compose up -d postgres

sudo /usr/local/bin/docker-compose up -d rundeck

cd .. (Volta para WebGIS-Platform)

10.2 - Subir Base do WebGIS

sudo /usr/local/bin/docker-compose up -d mercator_db

10.2.1 - Carregar base de dados (ainda não executado 27jun2022)
```bash
cp dump.sql ./db
docker-compose exec mercator_db bash
mysql -u root –p 'm3rc4t0r##' mercator_db < /var/lib/mysql/dump.sql
```

**Observação**: Caso o passo anterior não funcione será necessário usar uma ferramenta auxiliar para carregar os dados no banco do mysql.

10.3 - Subir Base de Backup

sudo /usr/local/bin/docker-compose up -d db-dbbackups


#Não precisa Subir Webserver. O frontend já sobe o nginx

#sudo /usr/local/bin/docker-compose up -d webserver

11 - Subir Geoserver

sudo /usr/local/bin/docker-compose up -d geoserver


