# Instalação Mercator

Antes de mais nada, vale lembrar que é necessário deixar nesta máquina rodando o GeoServer com as camadas.

Após subir o backend, as camadas tem que ser configuradas na interface disponibilizada pelo CMS *Strapi* localizado em: `<domínio da aplicação>:1337/admin`

A aplicação do **Modelo Lagrangiano** também deve ser adicionado a máquina ao qual irá rodar o simulador.

1 - Clonar Projeto

2 - Instalar Node JS

```bash
curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
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
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

5 - Subir webserver (Oil Spill tool)

```bash
cd ./mercator-server
npm install && npm run build
# export SPREAD_OIL_PATH=<caminho para a ferramenta do modelo lagrangiano>
# como por exemplo: 
export SPREAD_OIL_PATH=/home/maretec/Lagrangian_Global/BSO
npm start
```

**Atenção:** A partir daqui todos os comando foram executado com permissão de administrador no servido usando: `sudo su`

6 - Subir Backend

```bash
cd ./mercator
docker-compose up backend -d
```

7 - Instalar PM2

```bash
npm install pm2 -g
```

8 - Subir Frontend

```bash
docker-compose up -d frontend
```

9 - Carregar base de dados

```bash
cp dump.sql ./db
docker-compose exec mercator_db bash
mysql -u root –p 'm3rc4t0r##' mercator_db < /var/lib/mysql/dump.sql
```

**Observação**: Caso o passo anterior não funcione será necessário usar uma ferramenta auxiliar para carregar os dados no banco do mysql.

