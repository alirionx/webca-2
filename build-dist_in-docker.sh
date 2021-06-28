#/bin/bash


TS=$(date +%s%N)
CONNAME=npmbuild_$TS
NODESRC=https://deb.nodesource.com/setup_16.x


docker run -itd --name $CONNAME ubuntu:focal
docker cp ./spa $CONNAME:/data

docker exec -it $CONNAME apt update
docker exec -it $CONNAME apt install -y curl
docker exec -it $CONNAME curl -sL $NODESRC -o /tmp/nodesource_setup.sh
docker exec -it $CONNAME chmod +x /tmp/nodesource_setup.sh
docker exec -it $CONNAME /tmp/nodesource_setup.sh
docker exec -it -e DEBIAN_FRONTEND=noninteractive $CONNAME apt install -y nodejs
docker exec -it $CONNAME node --version

docker exec -it -w /data $CONNAME npm install
docker exec -it -w /data $CONNAME npm run build

docker cp $CONNAME:/data/dist ./webapp/

docker kill $CONNAME
docker rm $CONNAME


