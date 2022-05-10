# Instalação Mercator

Antes de mais nada, vale lembrar que é necessário deixar nesta máquina rodando o GeoServer com as camadas.

Após subir o backend, as camadas tem que ser configuradas na interface disponibilizada pelo CMS *Strapi* localizado em: `<domínio da aplicação>:1337/admin`

A aplicação do **Modelo Lagrangiano** também deve ser adicionado a máquina ao qual irá rodar o simulador.

1 - Clonar Projeto
git clone https://github.com/Brazilian-Sea-Observatory/WebGIS-Platform.git

1.1 - Ir para o branch de construção mais atual: buildingAAMMx, AA=ano, MM=mês, x=a,b,c,...
git checkout building2205a

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

5 - Subir webserver (Oil Spill tool)

```bash
cd ./mercator-server
npm install
TODO: O npm install está emitindo vários avisos de deprecated e vulnerabilidades. Isto se dá porque os packege.json estão com versões de bibliotecas js antigas. Por enquanto não vamos alterar (ou atualizar) essas bibliotecas, pois a prioridade é manter o WebGIS original para chegar em uma versão operacional. Depois procederemos paulatinamente as atualizações.

npm run build
# export SPREAD_OIL_PATH=<caminho para a ferramenta do modelo lagrangiano>
# como por exemplo: 
export SPREAD_OIL_PATH=/home/maretec/Lagrangian_Global/BSO
npm start
```


**Atenção:** A partir daqui todos os comandos foram executados com permissão de administrador no servido usando: `sudo su`

6 - Subir Backend

```bash
cd ./mercator
docker-compose up backend -d
```

7 - Instalar PM2

```bash
Verificar se o branch trouxe o link simbólico. Caso esteja faltando, criá-lo com o comando ln
cd src
WebGIS-Platform/mercator-server/src$ ln -s ../dist/index.js
cd ..
WebGIS-Platform/mercator-server$ sudo npm install -g pm2
WebGIS-Platform/mercator-server$ sudo pm2 start ecosystem.config.js
```

8 - Subir Frontend

```bash
docker-compose up -d frontend
```

sudo /usr/local/bin/docker-compose up -d scripts

9 - Carregar base de dados

```bash
cp dump.sql ./db
docker-compose exec mercator_db bash
mysql -u root –p 'm3rc4t0r##' mercator_db < /var/lib/mysql/dump.sql
```

**Observação**: Caso o passo anterior não funcione será necessário usar uma ferramenta auxiliar para carregar os dados no banco do mysql.

10 - Instalar GeoServer versão 2.16.1 e iniciar o serviço através do script startup.sh no diretório **./var/www/geoserver-2.16.1/bin**

sudo mkdir /var/www
Instalar o GeoServer 2.16.1 em /var/www
Copiar o scritp WebGIS-Platform/var_www_geoserver-2.16.1_bin_startup.sh para /var/www/geoserver-2.16.1/bin/startup.sh
Executar o script
/var/www/geoserver-2.16.1/bin/startup.sh
