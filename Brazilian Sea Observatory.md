# Brazilian Sea Observatory

Observatório do mar da costa brasileira desenvolvido com a seguinte Stack:

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

## Instalação

Toda a aplicação, exceto a parte que comunica com a ferramenta do modelo de espalhamento de óleo roda dentro de containers Docker e estão configuradas no arquivo: **docker-compose.yml**.

É possível levantar os serviços individualmente (recomendado) ou todos os serviços de uma única vez com o comando: `docker-compose up -d`.

Para subir individualmente, rode os seguintes comandos:

```bash
docker-compose up -d frontend
docker-compose up -d backend
```

### Serviço de espalhamento de óleo

Devido a integração com aplicações externas e da necessidade de rodar com permissões de superusuário, a aplicação de integração com a ferramenta de cálculo do espalhamento é executado separadamente.

Para executar, acesse o diretório **./mercator-server** e rode os comandos:

```bash
npm install
npm run build
sudo npm install -g pm2
sudo pm2 start ecosystem.config.js
```

### GeoServer

A instalação do serviço de amazenamento de camadas pode ser acessado através do diretório **./var/www/geoserver*/bin** e o seguinte comando para iniciar o serviço:

```bash
./startup.sh
```

Adicionalmente à aplicação temos alguns scripts que rodam diariamente para manter a aplicação atualizada

#### Atualização das Camadas

O primeiro script localizado em: **/home/maretec/mercator/** busca atualizações das camadas Globais através da conexão com a Copernicus e também copia os novos arquivos disponibilizados via FTP dos modelos regionais é necessário executar o seguinte comando:

```bash
/usr/local/bin/docker-compose exec scripts /bin/bash /home/geoserver/mercator_routine_products/routineMercatorOperational.sh
```

### Conversão NCs em JSON (Streamlines)

O segundo script localizado em **/home/maretec/mercator/** converte alguns arquivos em NetCDF para JSON assim é possível executar a animação das correntes marítimas em Streamlines, usa o seguinte comando para execução:

```bash
/usr/local/bin/docker-compose up jupyter
```

### Drifiting Bouys Download 

O último e terceiro script, localizado em **/home/maretec**, busca a atualização das estações de monitoramento e driting bouys que serão representadas na plataforma através do seguinte comando:

```bash
python3 /home/maretec/downloadDriftingBuoysData.py
```